from django.contrib import admin
from .models import Campaign, Donor, Donation

admin.site.site_header = "Q-FundTrack Administration"
admin.site.site_title = "Q-FundTrack Admin Portal"
admin.site.index_title = "Donation & Campaign Management Dashboard"


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'target_amount', 'get_amount_raised', 'get_progress', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'start_date', 'end_date')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    fieldsets = (
        ('Campaign Information', {
            'fields': ('name', 'description', 'status')
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
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'get_total_donated', 'get_donation_count', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)

    @admin.display(description="Total Contributed (₹)")
    def get_total_donated(self, obj):
        return f"₹{obj.total_donated:,.2f}"

    @admin.display(description="Total Donations")
    def get_donation_count(self, obj):
        return obj.donation_count


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('reference', 'donor', 'campaign', 'amount_display', 'payment_method', 'donation_date')
    list_filter = ('payment_method', 'campaign', 'donation_date')
    search_fields = ('reference', 'donor__name', 'donor__email', 'campaign__name')
    date_hierarchy = 'donation_date'
    autocomplete_fields = ('donor', 'campaign')

    @admin.display(description="Amount (₹)")
    def amount_display(self, obj):
        return f"₹{obj.amount:,.2f}"

