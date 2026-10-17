from django.db import migrations

def create_default_organization_and_assign(apps, schema_editor):
    Organization = apps.get_model('tracker', 'Organization')
    UserProfile = apps.get_model('tracker', 'UserProfile')
    Campaign = apps.get_model('tracker', 'Campaign')
    Donor = apps.get_model('tracker', 'Donor')
    Donation = apps.get_model('tracker', 'Donation')
    User = apps.get_model('auth', 'User')

    # 1. Create or get default Organization
    default_org, created = Organization.objects.get_or_create(
        code='DEFAULT-ORG',
        defaults={
            'name': 'Global FundTrack NGO',
        }
    )

    # 2. Attach existing users (like superuser 'admin') to default_org as ORG_ADMIN
    for user in User.objects.all():
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'organization': default_org,
                'role': 'ORG_ADMIN',
            }
        )

    # 3. Attach existing campaigns to default_org
    Campaign.objects.filter(organization__isnull=True).update(organization=default_org)

    # 4. Attach existing donors to default_org
    Donor.objects.filter(organization__isnull=True).update(organization=default_org)

    # 5. Attach existing donations to default_org
    Donation.objects.filter(organization__isnull=True).update(organization=default_org)


def reverse_default_org(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_organization_alter_donor_email_campaign_organization_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_organization_and_assign, reverse_code=reverse_default_org),
    ]
