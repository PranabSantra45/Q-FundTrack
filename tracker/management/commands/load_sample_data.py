from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from tracker.models import Campaign, Donor, Donation


class Command(BaseCommand):
    help = 'Populates the database with sample campaigns, donors, donations, and superuser for 0th review demo'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Initializing Q-FundTrack sample data...'))

        # 1. Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@qfundtrack.local', 'is_staff': True, 'is_superuser': True}
        )
        admin_user.set_password('admin123')
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        if created:
            self.stdout.write(self.style.SUCCESS('Created default superuser: admin / admin123'))
        else:
            self.stdout.write(self.style.SUCCESS('Verified superuser credentials: admin / admin123'))

        # 2. Campaigns
        now = timezone.now().date()
        campaigns_data = [
            {
                'name': 'Education Support',
                'description': 'Providing school kits, scholarships, and academic support to underprivileged students across rural and semi-urban communities.',
                'target_amount': Decimal('150000.00'),
                'start_date': now - timedelta(days=20),
                'end_date': now + timedelta(days=40),
                'status': 'ACTIVE',
            },
            {
                'name': 'Medical Assistance',
                'description': 'Emergency healthcare assistance, diagnostic support, and critical medication subsidies for low-income families.',
                'target_amount': Decimal('200000.00'),
                'start_date': now - timedelta(days=15),
                'end_date': now + timedelta(days=45),
                'status': 'ACTIVE',
            },
            {
                'name': 'Digital Literacy',
                'description': 'Setting up community computer labs and conducting coding & vocational digital skills workshops for youth.',
                'target_amount': Decimal('100000.00'),
                'start_date': now - timedelta(days=10),
                'end_date': now + timedelta(days=50),
                'status': 'ACTIVE',
            },
        ]

        campaign_objs = {}
        for cdata in campaigns_data:
            camp, _ = Campaign.objects.update_or_create(
                name=cdata['name'],
                defaults=cdata
            )
            campaign_objs[camp.name] = camp
            self.stdout.write(f' - Campaign: {camp.name} (Target: Rs {camp.target_amount:,.2f})')

        # 3. Donors
        donors_data = [
            {'name': 'Rahul Sharma', 'email': 'rahul.sharma@example.com', 'phone': '+91 98112 34567', 'address': 'Indiranagar, Bengaluru'},
            {'name': 'Anita Roy', 'email': 'anita.roy@example.com', 'phone': '+91 98223 45678', 'address': 'Salt Lake Sector 5, Kolkata'},
            {'name': 'Arjun Das', 'email': 'arjun.das@example.com', 'phone': '+91 98334 56789', 'address': 'Bandra West, Mumbai'},
            {'name': 'Priya Sen', 'email': 'priya.sen@example.com', 'phone': '+91 98445 67890', 'address': 'Connaught Place, New Delhi'},
        ]

        donor_objs = {}
        for ddata in donors_data:
            donor, _ = Donor.objects.update_or_create(
                email=ddata['email'],
                defaults=ddata
            )
            donor_objs[donor.name] = donor
            self.stdout.write(f' - Donor: {donor.name} ({donor.email})')

        # 4. Donations (fictional sample records)
        donations_data = [
            {
                'reference': 'TXN-EDU-001',
                'donor': donor_objs['Rahul Sharma'],
                'campaign': campaign_objs['Education Support'],
                'amount': Decimal('25000.00'),
                'payment_method': 'UPI',
                'notes': 'Quarterly scholarship contribution',
            },
            {
                'reference': 'TXN-MED-002',
                'donor': donor_objs['Anita Roy'],
                'campaign': campaign_objs['Medical Assistance'],
                'amount': Decimal('35000.00'),
                'payment_method': 'NETBANKING',
                'notes': 'Dedicated to emergency pediatric fund',
            },
            {
                'reference': 'TXN-DIG-003',
                'donor': donor_objs['Arjun Das'],
                'campaign': campaign_objs['Digital Literacy'],
                'amount': Decimal('15000.00'),
                'payment_method': 'CARD',
                'notes': 'Funding computer lab monitors',
            },
            {
                'reference': 'TXN-EDU-004',
                'donor': donor_objs['Priya Sen'],
                'campaign': campaign_objs['Education Support'],
                'amount': Decimal('30000.00'),
                'payment_method': 'UPI',
                'notes': 'Annual books and kits donation',
            },
            {
                'reference': 'TXN-MED-005',
                'donor': donor_objs['Rahul Sharma'],
                'campaign': campaign_objs['Medical Assistance'],
                'amount': Decimal('20000.00'),
                'payment_method': 'UPI',
                'notes': 'Medicines subsidy contribution',
            },
            {
                'reference': 'TXN-DIG-006',
                'donor': donor_objs['Anita Roy'],
                'campaign': campaign_objs['Digital Literacy'],
                'amount': Decimal('22000.00'),
                'payment_method': 'CARD',
                'notes': 'Internet connectivity setup support',
            },
        ]

        for don in donations_data:
            d_obj, _ = Donation.objects.update_or_create(
                reference=don['reference'],
                defaults=don
            )
            self.stdout.write(f' - Donation: Rs {d_obj.amount:,.2f} from {d_obj.donor.name} -> {d_obj.campaign.name}')

        self.stdout.write(self.style.SUCCESS("""
======================================================
 Sample data loaded successfully!
 Superuser created:
   Username: admin
   Password: admin123
   Login URL: http://127.0.0.1:8000/admin/
======================================================
"""))
