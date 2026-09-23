from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal
from .models import Campaign, Donor, Donation
from .forms import DonationForm, CampaignForm, DonorForm


def dashboard(request):
    total_campaigns = Campaign.objects.count()
    active_campaigns = Campaign.objects.filter(status='ACTIVE').count()
    total_donors = Donor.objects.count()
    total_donations = Donation.objects.count()
    total_amount_donated = Donation.objects.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    campaigns = Campaign.objects.all()
    recent_donations = Donation.objects.select_related('donor', 'campaign')[:8]

    context = {
        'total_campaigns': total_campaigns,
        'active_campaigns': active_campaigns,
        'total_donors': total_donors,
        'total_donations': total_donations,
        'total_amount_donated': total_amount_donated,
        'campaigns': campaigns,
        'recent_donations': recent_donations,
    }
    return render(request, 'dashboard.html', context)


def campaign_list(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save()
            messages.success(request, f'Campaign "{campaign.name}" created successfully!')
            return redirect('campaign_list')
        else:
            messages.error(request, 'Please correct the errors in the campaign form.')
    else:
        form = CampaignForm()

    campaigns = Campaign.objects.all()
    context = {
        'campaigns': campaigns,
        'form': form,
    }
    return render(request, 'campaigns.html', context)


def donation_list(request):
    donation_form = DonationForm()
    donor_form = DonorForm()

    if request.method == 'POST':
        action = request.POST.get('action', 'create_donation')

        if action == 'create_donor':
            donor_form = DonorForm(request.POST)
            if donor_form.is_valid():
                donor = donor_form.save()
                messages.success(request, f'New Donor "{donor.name}" registered successfully! You can now record their donation.')
                return redirect('donation_list')
            else:
                messages.error(request, 'Could not register donor. Check the inputs.')
        else:
            donation_form = DonationForm(request.POST)
            if donation_form.is_valid():
                donation = donation_form.save()
                messages.success(request, f'Donation of ₹{donation.amount:,.2f} recorded successfully for "{donation.campaign.name}" (Ref: {donation.reference})!')
                return redirect('donation_list')
            else:
                messages.error(request, 'Could not record donation. Please check the form.')

    donations = Donation.objects.select_related('donor', 'campaign')[:50]
    context = {
        'donations': donations,
        'donation_form': donation_form,
        'donor_form': donor_form,
    }
    return render(request, 'donations.html', context)

