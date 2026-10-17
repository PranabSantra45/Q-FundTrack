from django.contrib import admin
from .models import Campaign, Donor, Donation, Organization, UserProfile

admin.site.site_header = "Q-FundTrack Administration"
admin.site.site_title = "Q-FundTrack Admin Portal"
admin.site.index_title = "Multi-Organization Donation & Campaign Management"


class TenantScopedAdmin(admin.ModelAdmin):
    """
    Base ModelAdmin enforcing multi-organization isolation.
    Superusers can view and manage all records.
    Non-superusers only see records belonging to their assigned organization.
    """
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile') and request.user.profile.organization:
            return qs.filter(organization=request.user.profile.organization)
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.organization:
            org = request.user.profile.organization
            if db_field.name in ['donor', 'campaign', 'organization']:
                kwargs['queryset'] = db_field.remote_field.model.objects.filter(organization=org)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser and hasattr(request.user, 'profile') and request.user.profile.organization:
            if hasattr(obj, 'organization') and not obj.organization_id:
                obj.organization = request.user.profile.organization
        super().save_model(request, obj, form, change)


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'member_count', 'campaign_count', 'created_at')
    search_fields = ('name', 'code')
    readonly_fields = ('created_at',)

    def member_count(self, obj):
        return obj.members.count()

    def campaign_count(self, obj):
        return obj.campaigns.count()

    def has_module_permission(self, request):
        # Only superusers or org admins can view the Organization directory in Admin
        if request.user.is_superuser:
            return True
        return hasattr(request.user, 'profile') and request.user.profile.is_admin

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile') and request.user.profile.organization:
            return qs.filter(pk=request.user.profile.organization.pk)
        return qs.none()


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'created_at')
    list_filter = ('role', 'organization')
    search_fields = ('user__username', 'user__email', 'organization__name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        if hasattr(request.user, 'profile') and request.user.profile.organization:
            return qs.filter(organization=request.user.profile.organization)
        return qs.none()


@admin.register(Campaign)
class CampaignAdmin(TenantScopedAdmin):
    list_display = ('name', 'organization', 'target_amount', 'get_amount_raised', 'get_progress', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'organization', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Campaign Information', {
            'fields': ('organization', 'name', 'description', 'status')
        }),
        ('Financial Goal', {
            'fields': ('target_amount',)
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'created_at')
        }),
    )

    @admin.display(description="Amount Raised (₹)")
    def get_amount_raised(self, obj):
        return f"₹{obj.amount_raised:,.2f}"

    @admin.display(description="Progress (%)")
    def get_progress(self, obj):
        return f"{obj.progress_percentage}%"


@admin.register(Donor)
class DonorAdmin(TenantScopedAdmin):
    list_display = ('name', 'organization', 'email', 'phone', 'get_total_donated', 'get_donation_count', 'created_at')
    list_filter = ('organization',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

    @admin.display(description="Total Contributed (₹)")
    def get_total_donated(self, obj):
        return f"₹{obj.total_donated:,.2f}"

    @admin.display(description="Total Donations")
    def get_donation_count(self, obj):
        return obj.donation_count


@admin.register(Donation)
class DonationAdmin(TenantScopedAdmin):
    list_display = ('reference', 'organization', 'donor', 'campaign', 'amount_display', 'payment_method', 'donation_date')
    list_filter = ('organization', 'payment_method', 'campaign', 'donation_date')
    search_fields = ('reference', 'donor__name', 'donor__email', 'campaign__name')
    date_hierarchy = 'donation_date'

    @admin.display(description="Amount (₹)")
    def amount_display(self, obj):
        return f"₹{obj.amount:,.2f}"


