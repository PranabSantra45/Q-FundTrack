from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum, Count
from decimal import Decimal

from .models import Campaign, Donor, Donation, Organization, UserProfile
from .forms import (
    DonationForm,
    CampaignForm,
    DonorForm,
    OrganizationRegistrationForm,
    MemberCreationForm,
)
from .permissions import (
    login_required_org,
    role_required,
    get_user_org,
    get_user_profile,
    check_org_access,
)


def home(request):
    """
    Public homepage separate from the private dashboard.
    Displays platform overview, active public campaigns with progress,
    and aggregate stats WITHOUT exposing private donor details or individual transactions.
    """
    public_campaigns = Campaign.objects.filter(status='ACTIVE')[:6]
    total_active_campaigns = Campaign.objects.filter(status='ACTIVE').count()
    total_organizations = Organization.objects.count()

    context = {
        'public_campaigns': public_campaigns,
        'total_active_campaigns': total_active_campaigns,
        'total_organizations': total_organizations,
    }
    return render(request, 'home.html', context)


def register_org(request):
    """
    Safe setup procedure for creating a new Organization and assigning the registrant as ORG_ADMIN.
    Prevents unauthorized users from joining an existing NGO without admin invitation.
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = OrganizationRegistrationForm(request.POST)
        if form.is_valid():
            user, org = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome! Organization '{org.name}' ({org.code}) created successfully. You are logged in as Organization Admin."
            )
            return redirect('dashboard')
        else:
            messages.error(request, "Please resolve the errors below to register your organization.")
    else:
        form = OrganizationRegistrationForm()

    return render(request, 'register_org.html', {'form': form})


def login_view(request):
    """Standard user authentication."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    """Logs out user and redirects to public home."""
    logout(request)
    messages.info(request, "You have been logged out safely.")
    return redirect('home')


@login_required_org
def dashboard(request):
    """
    Private dashboard protected by authentication.
    Calculates totals and displays metrics ONLY for the current user's organization.
    """
    org = get_user_org(request.user)
    profile = get_user_profile(request.user)

    total_campaigns = Campaign.objects.filter(organization=org).count()
    active_campaigns = Campaign.objects.filter(organization=org, status='ACTIVE').count()
    total_donors = Donor.objects.filter(organization=org).count()
    total_donations = Donation.objects.filter(organization=org).count()
    total_amount_donated = (
        Donation.objects.filter(organization=org).aggregate(total=Sum('amount'))['total']
        or Decimal('0.00')
    )

    campaigns = Campaign.objects.filter(organization=org)
    recent_donations = Donation.objects.filter(organization=org).select_related('donor', 'campaign')[:8]

    context = {
        'org': org,
        'profile': profile,
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_amount_donated': total_amount_donated,
        'campaigns': campaigns,
        'recent_donations': recent_donations,
    }
    return render(request, 'dashboard.html', context)


@login_required_org
def campaign_list(request):
    """
    Lists campaigns for the user's organization and allows creation.
    """
    org = get_user_org(request.user)
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = CampaignForm(request.POST, organization=org)
        if form.is_valid():
            campaign = form.save()
            messages.success(request, f'Campaign "{campaign.name}" created successfully!')
            return redirect('campaign_list')
        else:
            messages.error(request, 'Please correct the errors in the campaign form.')
    else:
        form = CampaignForm(organization=org)

    campaigns = Campaign.objects.filter(organization=org)
    context = {
        'org': org,
        'profile': profile,
        'campaigns': campaigns,
        'form': form,
    }
    return render(request, 'campaigns.html', context)


@login_required_org
def campaign_detail(request, pk):
    """View campaign details; enforces organization isolation."""
    org = get_user_org(request.user)
    campaign = get_object_or_404(Campaign, pk=pk)
    check_org_access(campaign, org)

    donations = campaign.donations.filter(organization=org).select_related('donor')
    context = {
        'org': org,
        'campaign': campaign,
        'donations': donations,
    }
    return render(request, 'campaign_detail.html', context)


@login_required_org
@role_required(['ORG_ADMIN', 'FINANCE'])
def campaign_delete(request, pk):
    """Delete a campaign; restricted to ORG_ADMIN and FINANCE."""
    org = get_user_org(request.user)
    campaign = get_object_or_404(Campaign, pk=pk)
    check_org_access(campaign, org)

    if request.method == 'POST':
        name = campaign.name
        campaign.delete()
        messages.success(request, f'Campaign "{name}" has been deleted.')
        return redirect('campaign_list')

    return redirect('campaign_list')


@login_required_org
def donor_list(request):
    """Lists donors belonging to the user's organization."""
    org = get_user_org(request.user)
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = DonorForm(request.POST, organization=org)
        if form.is_valid():
            donor = form.save()
            messages.success(request, f'Donor "{donor.name}" registered successfully!')
            return redirect('donor_list')
        else:
            messages.error(request, 'Could not register donor. Check the inputs.')
    else:
        form = DonorForm(organization=org)

    donors = Donor.objects.filter(organization=org)
    context = {
        'org': org,
        'profile': profile,
        'donors': donors,
        'form': form,
    }
    return render(request, 'donors.html', context)


@login_required_org
@role_required(['ORG_ADMIN'])
def donor_delete(request, pk):
    """Delete donor; restricted to ORG_ADMIN."""
    org = get_user_org(request.user)
    donor = get_object_or_404(Donor, pk=pk)
    check_org_access(donor, org)

    if request.method == 'POST':
        name = donor.name
        donor.delete()
        messages.success(request, f'Donor "{name}" was removed.')
    return redirect('donor_list')


@login_required_org
def donation_list(request):
    """
    Lists donations and provides recording form scoped to current user's organization.
    """
    org = get_user_org(request.user)
    profile = get_user_profile(request.user)

    donation_form = DonationForm(organization=org)
    donor_form = DonorForm(organization=org)

    if request.method == 'POST':
        action = request.POST.get('action', 'create_donation')

        if action == 'create_donor':
            donor_form = DonorForm(request.POST, organization=org)
            if donor_form.is_valid():
                donor = donor_form.save()
                messages.success(request, f'New Donor "{donor.name}" registered successfully!')
                return redirect('donation_list')
            else:
                messages.error(request, 'Could not register donor. Check the inputs.')
        else:
            donation_form = DonationForm(request.POST, organization=org)
            if donation_form.is_valid():
                donation = donation_form.save()
                messages.success(
                    request,
                    f'Donation of ₹{donation.amount:,.2f} recorded for "{donation.campaign.name}" (Ref: {donation.reference})!'
                )
                return redirect('donation_list')
            else:
                messages.error(request, 'Could not record donation. Please check the form.')

    donations = Donation.objects.filter(organization=org).select_related('donor', 'campaign')[:50]
    context = {
        'org': org,
        'profile': profile,
        'donations': donations,
        'donation_form': donation_form,
        'donor_form': donor_form,
    }
    return render(request, 'donations.html', context)


@login_required_org
@role_required(['ORG_ADMIN', 'FINANCE'])
def donation_delete(request, pk):
    """Delete a donation entry; restricted to ORG_ADMIN and FINANCE."""
    org = get_user_org(request.user)
    donation = get_object_or_404(Donation, pk=pk)
    check_org_access(donation, org)

    if request.method == 'POST':
        ref = donation.reference
        donation.delete()
        messages.success(request, f'Donation record [{ref}] deleted successfully.')
    return redirect('donation_list')


@login_required_org
@role_required(['ORG_ADMIN'])
def organization_members(request):
    """
    Manage team members within the organization.
    Restricted to ORG_ADMIN.
    """
    org = get_user_org(request.user)
    profile = get_user_profile(request.user)

    if request.method == 'POST':
        form = MemberCreationForm(request.POST, organization=org)
        if form.is_valid():
            new_member = form.save()
            messages.success(
                request,
                f"Team member '{new_member.user.username}' added as {new_member.get_role_display()}."
            )
            return redirect('organization_members')
        else:
            messages.error(request, "Failed to create team member. Check input errors.")
    else:
        form = MemberCreationForm(organization=org)

    members = UserProfile.objects.filter(organization=org).select_related('user')
    context = {
        'org': org,
        'profile': profile,
        'members': members,
        'form': form,
    }
    return render(request, 'members.html', context)


