from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Sum
from django.core.exceptions import ValidationError
from decimal import Decimal


class Organization(models.Model):
    name = models.CharField(max_length=200, help_text="Official name of the organization / NGO")
    code = models.CharField(
        max_length=50,
        unique=True,
        db_index=True,
        help_text="Unique identifier code for the organization (e.g. HELP-AGE-IN)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"

    def __str__(self):
        return f"{self.name} ({self.code})"


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('ORG_ADMIN', 'Organization Admin'),
        ('FINANCE', 'Finance'),
        ('STAFF', 'Staff'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STAFF')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"{self.user.username} ({self.get_role_display()} @ {self.organization.name})"

    @property
    def is_admin(self) -> bool:
        return self.role == 'ORG_ADMIN' or self.user.is_superuser

    @property
    def is_finance(self) -> bool:
        return self.role in ['ORG_ADMIN', 'FINANCE'] or self.user.is_superuser


class Campaign(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('PAUSED', 'Paused'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='campaigns',
        help_text="Organization owning this campaign",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=200, help_text="Name of the fundraising campaign")
    description = models.TextField(help_text="Detailed description of the campaign objectives")
    target_amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Fundraising goal in INR")
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    def __str__(self):
        return self.name

    @property
    def amount_raised(self) -> Decimal:
        """Calculate total amount received from all donations for this campaign."""
        total = self.donations.aggregate(total=Sum('amount'))['total']
        return total if total is not None else Decimal('0.00')

    @property
    def progress_percentage(self) -> float:
        """Calculate percentage of target reached, capped at 100 for basic bar display."""
        if not self.target_amount or self.target_amount <= Decimal('0.00'):
            return 0.0
        pct = (self.amount_raised / self.target_amount) * Decimal('100.0')
        return round(float(pct), 1)

    @property
    def remaining_amount(self) -> Decimal:
        """Calculate remaining amount to reach target."""
        rem = self.target_amount - self.amount_raised
        return rem if rem > Decimal('0.00') else Decimal('0.00')

    @property
    def donor_count(self) -> int:
        """Number of unique donors who contributed to this campaign."""
        return self.donations.values('donor').distinct().count()


class Donor(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='donors',
        help_text="Organization managing this donor record",
        null=True,
        blank=True
    )
    name = models.CharField(max_length=150, help_text="Full name of the donor")
    email = models.EmailField(help_text="Primary contact email")
    phone = models.CharField(max_length=20, blank=True, help_text="Contact phone number")
    address = models.TextField(blank=True, help_text="Physical or billing address")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Donor"
        verbose_name_plural = "Donors"
        unique_together = ('organization', 'email')

    def __str__(self):
        return f"{self.name} ({self.email})"

    @property
    def total_donated(self) -> Decimal:
        """Calculate cumulative donations made by this donor."""
        total = self.donations.aggregate(total=Sum('amount'))['total']
        return total if total is not None else Decimal('0.00')

    @property
    def donation_count(self) -> int:
        """Count total contributions."""
        return self.donations.count()


class Donation(models.Model):
    PAYMENT_METHODS = [
        ('UPI', 'UPI / QR Code'),
        ('CARD', 'Credit / Debit Card'),
        ('NETBANKING', 'Net Banking'),
        ('CASH', 'Cash / Cheque'),
        ('BANK_TRANSFER', 'Direct Bank Transfer / NEFT'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='donations',
        help_text="Organization owning this donation record",
        null=True,
        blank=True
    )
    donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        related_name='donations',
        help_text="Donor who contributed this donation"
    )
    campaign = models.ForeignKey(
        Campaign,
        on_delete=models.CASCADE,
        related_name='donations',
        help_text="Target campaign receiving the funds"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Donation amount in INR")
    donation_date = models.DateTimeField(default=timezone.now, help_text="Date and time when donation was received")
    payment_method = models.CharField(max_length=30, choices=PAYMENT_METHODS, default='UPI')
    reference = models.CharField(max_length=100, unique=True, help_text="Transaction reference number or receipt ID")
    notes = models.TextField(blank=True, help_text="Optional remarks or donor message")

    class Meta:
        ordering = ['-donation_date']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"

    def __str__(self):
        return f"₹{self.amount} by {self.donor.name} to {self.campaign.name} [Ref: {self.reference}]"

    def clean(self):
        super().clean()
        if self.donor_id and self.organization_id and self.donor.organization_id and self.donor.organization_id != self.organization_id:
            raise ValidationError("Donor belongs to a different organization.")
        if self.campaign_id and self.organization_id and self.campaign.organization_id and self.campaign.organization_id != self.organization_id:
            raise ValidationError("Campaign belongs to a different organization.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


