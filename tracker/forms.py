from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Campaign, Donor, Donation, Organization, UserProfile
import uuid


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['donor', 'campaign', 'amount', 'payment_method', 'reference', 'notes']
        widgets = {
            'donor': forms.Select(attrs={'class': 'form-select'}),
            'campaign': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 5000', 'step': '0.01', 'min': '1'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. UPI-982347102938'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Optional remarks / message'}),
        }

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)
        if not self.initial.get('reference'):
            self.initial['reference'] = f'TXN-{uuid.uuid4().hex[:8].upper()}'
        if self.organization:
            self.fields['donor'].queryset = Donor.objects.filter(organization=self.organization)
            self.fields['campaign'].queryset = Campaign.objects.filter(organization=self.organization)

    def clean(self):
        cleaned_data = super().clean()
        donor = cleaned_data.get('donor')
        campaign = cleaned_data.get('campaign')

        if donor and self.organization and donor.organization != self.organization:
            raise ValidationError("Selected donor does not belong to your organization.")
        if campaign and self.organization and campaign.organization != self.organization:
            raise ValidationError("Selected campaign does not belong to your organization.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.organization:
            instance.organization = self.organization
        if commit:
            instance.save()
        return instance


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'description', 'target_amount', 'start_date', 'end_date', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Campaign Name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Campaign objectives...'}),
            'target_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Target in INR', 'step': '100', 'min': '100'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.organization:
            instance.organization = self.organization
        if commit:
            instance.save()
        return instance


class DonorForm(forms.ModelForm):
    class Meta:
        model = Donor
        fields = ['name', 'email', 'phone', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'name@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+91 9876543210'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'City, State'}),
        }

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.organization:
            qs = Donor.objects.filter(organization=self.organization, email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise ValidationError("A donor with this email already exists in your organization.")
        return email

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.organization:
            instance.organization = self.organization
        if commit:
            instance.save()
        return instance


class OrganizationRegistrationForm(forms.Form):
    organization_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Hope Foundation India'})
    )
    organization_code = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. HOPE-IN (Letters & hyphens)'})
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Choose username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'admin@yourngo.org'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Strong password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repeat password'})
    )

    def clean_organization_code(self):
        code = self.cleaned_data.get('organization_code').upper().strip()
        if Organization.objects.filter(code=code).exists():
            raise ValidationError("This organization identifier code is already registered.")
        return code

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        confirm = cleaned_data.get('confirm_password')
        if pwd and confirm and pwd != confirm:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data

    def save(self):
        org = Organization.objects.create(
            name=self.cleaned_data['organization_name'],
            code=self.cleaned_data['organization_code']
        )
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data.get('last_name', ''),
            password=self.cleaned_data['password']
        )
        UserProfile.objects.create(
            user=user,
            organization=org,
            role='ORG_ADMIN'
        )
        return user, org


class MemberCreationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'})
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def save(self):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data.get('last_name', ''),
            password=self.cleaned_data['password']
        )
        profile = UserProfile.objects.create(
            user=user,
            organization=self.organization,
            role=self.cleaned_data['role']
        )
        return profile

