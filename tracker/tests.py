from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from decimal import Decimal
from datetime import date, timedelta

from tracker.models import Organization, UserProfile, Campaign, Donor, Donation


class MultiOrganizationSecurityTests(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Organization A and Users
        self.org_a = Organization.objects.create(name="Hope Foundation", code="HOPE-A")
        self.admin_a = User.objects.create_user(username="admin_a", password="password123")
        self.profile_admin_a = UserProfile.objects.create(
            user=self.admin_a, organization=self.org_a, role="ORG_ADMIN"
        )

        self.staff_a = User.objects.create_user(username="staff_a", password="password123")
        self.profile_staff_a = UserProfile.objects.create(
            user=self.staff_a, organization=self.org_a, role="STAFF"
        )

        # 2. Organization B and Users
        self.org_b = Organization.objects.create(name="Care Trust", code="CARE-B")
        self.admin_b = User.objects.create_user(username="admin_b", password="password123")
        self.profile_admin_b = UserProfile.objects.create(
            user=self.admin_b, organization=self.org_b, role="ORG_ADMIN"
        )

        # 3. Records for Org A
        today = date.today()
        self.campaign_a = Campaign.objects.create(
            organization=self.org_a,
            name="Org A Education",
            description="Campaign A description",
            target_amount=Decimal("10000.00"),
            start_date=today,
            end_date=today + timedelta(days=30),
            status="ACTIVE",
        )
        self.donor_a = Donor.objects.create(
            organization=self.org_a,
            name="Donor A",
            email="donor_a@example.com",
            phone="9876543210",
        )
        self.donation_a = Donation.objects.create(
            organization=self.org_a,
            campaign=self.campaign_a,
            donor=self.donor_a,
            amount=Decimal("2500.00"),
            payment_method="UPI",
            reference="TXN-A-001",
        )

        # 4. Records for Org B
        self.campaign_b = Campaign.objects.create(
            organization=self.org_b,
            name="Org B Health",
            description="Campaign B description",
            target_amount=Decimal("20000.00"),
            start_date=today,
            end_date=today + timedelta(days=30),
            status="ACTIVE",
        )
        self.donor_b = Donor.objects.create(
            organization=self.org_b,
            name="Donor B",
            email="donor_b@example.com",
            phone="9876543211",
        )
        self.donation_b = Donation.objects.create(
            organization=self.org_b,
            campaign=self.campaign_b,
            donor=self.donor_b,
            amount=Decimal("5000.00"),
            payment_method="CARD",
            reference="TXN-B-001",
        )

    def test_public_homepage_and_privacy(self):
        """Public homepage shows high-level stats without private donor details or individual transactions."""
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        # Campaign names are visible
        self.assertIn("Org A Education", content)
        self.assertIn("Org B Health", content)
        # Private donor info and transaction references MUST NOT be exposed
        self.assertNotIn("donor_a@example.com", content)
        self.assertNotIn("TXN-A-001", content)
        self.assertNotIn("TXN-B-001", content)

    def test_unauthenticated_dashboard_redirect(self):
        """Unauthenticated requests to private dashboard must redirect to login."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('login'), response.url)

    def test_dashboard_isolation(self):
        """User A sees only Org A totals and records, never Org B totals."""
        self.client.login(username="admin_a", password="password123")
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)

        # Org A records present
        self.assertContains(response, "HOPE-A")
        self.assertContains(response, "Org A Education")
        self.assertContains(response, "2500.00")

        # Org B records absent
        self.assertNotContains(response, "CARE-B")
        self.assertNotContains(response, "Org B Health")
        self.assertNotContains(response, "TXN-B-001")

        # Context aggregates check
        self.assertEqual(response.context['total_amount_donated'], Decimal("2500.00"))
        self.assertEqual(response.context['total_campaigns'], 1)
        self.assertEqual(response.context['total_donors'], 1)
        self.assertEqual(response.context['total_donations'], 1)

    def test_url_tampering_campaign_detail_forbidden(self):
        """User A attempting to access Org B campaign detail via URL ID gets 403 Forbidden."""
        self.client.login(username="admin_a", password="password123")
        response = self.client.get(reverse('campaign_detail', args=[self.campaign_b.pk]))
        self.assertEqual(response.status_code, 403)

    def test_url_tampering_campaign_delete_forbidden(self):
        """User A attempting to delete Org B campaign via URL ID gets 403 Forbidden."""
        self.client.login(username="admin_a", password="password123")
        response = self.client.post(reverse('campaign_delete', args=[self.campaign_b.pk]))
        self.assertEqual(response.status_code, 403)
        # Verify campaign B was NOT deleted
        self.assertTrue(Campaign.objects.filter(pk=self.campaign_b.pk).exists())

    def test_url_tampering_donor_delete_forbidden(self):
        """User A attempting to delete Org B donor via URL ID gets 403 Forbidden."""
        self.client.login(username="admin_a", password="password123")
        response = self.client.post(reverse('donor_delete', args=[self.donor_b.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Donor.objects.filter(pk=self.donor_b.pk).exists())

    def test_url_tampering_donation_delete_forbidden(self):
        """User A attempting to delete Org B donation via URL ID gets 403 Forbidden."""
        self.client.login(username="admin_a", password="password123")
        response = self.client.post(reverse('donation_delete', args=[self.donation_b.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Donation.objects.filter(pk=self.donation_b.pk).exists())

    def test_form_isolation_cross_organization_donation_blocked(self):
        """DonationForm rejects attempts to associate Org B donor or campaign into Org A."""
        self.client.login(username="admin_a", password="password123")

        # Attempt to record donation with Org B's campaign
        payload = {
            'donor': self.donor_a.pk,
            'campaign': self.campaign_b.pk,  # Cross-org injection attempt
            'amount': '1000.00',
            'payment_method': 'UPI',
            'reference': 'TXN-HACK-001',
            'action': 'create_donation',
        }
        response = self.client.post(reverse('donation_list'), data=payload)
        # Form should fail validation and not create record
        self.assertFalse(Donation.objects.filter(reference='TXN-HACK-001').exists())

    def test_role_based_access_staff_cannot_delete_campaign(self):
        """Staff user in Org A cannot delete Org A's campaign (403 Forbidden)."""
        self.client.login(username="staff_a", password="password123")
        response = self.client.post(reverse('campaign_delete', args=[self.campaign_a.pk]))
        self.assertEqual(response.status_code, 403)
        self.assertTrue(Campaign.objects.filter(pk=self.campaign_a.pk).exists())

    def test_role_based_access_admin_can_delete_campaign(self):
        """Org Admin in Org A can successfully delete Org A's campaign."""
        self.client.login(username="admin_a", password="password123")
        response = self.client.post(reverse('campaign_delete', args=[self.campaign_a.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Campaign.objects.filter(pk=self.campaign_a.pk).exists())

    def test_registration_creates_new_org_and_admin(self):
        """User registration creates a new organization and assigns registrant as ORG_ADMIN."""
        payload = {
            'organization_name': 'Solar Future Trust',
            'organization_code': 'SOLAR-IN',
            'username': 'solar_admin',
            'email': 'admin@solar.org',
            'first_name': 'Solar',
            'last_name': 'Admin',
            'password': 'SecurePassword123!',
            'confirm_password': 'SecurePassword123!',
        }
        response = self.client.post(reverse('register_org'), data=payload)
        self.assertEqual(response.status_code, 302)

        # Check DB
        new_org = Organization.objects.get(code='SOLAR-IN')
        self.assertEqual(new_org.name, 'Solar Future Trust')
        new_user = User.objects.get(username='solar_admin')
        self.assertEqual(new_user.profile.organization, new_org)
        self.assertEqual(new_user.profile.role, 'ORG_ADMIN')

