# Q-FundTrack: Cloud-Based Donation & Campaign Management System

A secure, multi-organization fundraising and campaign tracking platform built with Python and Django. Designed for nonprofit organizations, charities, and trusts to manage campaigns, donors, and donation ledgers with strict multi-tenant data isolation and Role-Based Access Control (RBAC).

---

## 1. Project Overview & Architecture

Q-FundTrack supports **multiple independent nonprofit organizations (NGOs)** within a single installation:
- **Tenant Isolation**: Each Organization operates in an isolated workspace. Campaigns, donors, and donations belong strictly to their owning organization.
- **Privacy Separation**: A public homepage showcases active community causes without exposing private donor names, contact details, or individual donation transactions.
- **Role-Based Access Control (RBAC)**: Each user within an organization holds a specific role:
  - **Organization Admin (`ORG_ADMIN`)**: Full administrative control, team member onboarding, campaign/donor/donation creation and deletion.
  - **Finance (`FINANCE`)**: Financial management, donation recording, audit inspection, and transaction removal.
  - **Staff (`STAFF`)**: Operational data entry (viewing campaigns & donors, recording donations). Blocked from deletion actions and member administration.
- **Django Admin Isolation**: Superusers retain global administrative visibility, while organization admins only see records within their organization's scope.

---

## 2. Technology Stack

### Currently Implemented (Local Multi-Tenant Backend)
- **Backend Framework**: Python 3.13, Django 6.1
- **Database**: SQLite (`db.sqlite3` with Django ORM multi-tenant scoping)
- **Frontend**: HTML5, Vanilla CSS / Bootstrap 5.3, Bootstrap Icons
- **Security & RBAC**: Custom decorators, scoped forms, URL tampering protection

### Planned Cloud Architecture (Phase 2 Roadmap)
- **Compute**: AWS EC2 with Gunicorn & Nginx
- **Database**: AWS RDS (PostgreSQL managed cloud database)
- **Storage**: AWS S3 (Bucket storage for campaign banners & PDF receipts)
- **Messaging**: AWS SNS (Automated SMS and Email donation alerts)

---

## 3. How to Run Locally

### Step 1: Open Terminal in Project Directory
```powershell
cd "C:\Users\Pranab Santra\Desktop\Projects\Qu-FundMe -- AWS Cloud"
```

### Step 2: Start Development Server
```powershell
.\qfund_env\Scripts\python manage.py runserver
```

Open your browser at:
- **Public Homepage**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Staff Sign In**: [http://127.0.0.1:8000/login/](http://127.0.0.1:8000/login/)
- **Register New NGO**: [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 4. Default Login & Test Credentials

### Existing Pre-Configured Administrator:
- **Username**: `admin`
- **Password**: `admin123`
- **Organization**: `Global FundTrack NGO` (Code: `DEFAULT-ORG`)
- **Access Level**: Full Organization Admin & Django Superuser

### Registering a New NGO (Self-Service Onboarding):
1. Navigate to [http://127.0.0.1:8000/register/](http://127.0.0.1:8000/register/).
2. Fill in:
   - **Organization Name**: e.g., `Hope Relief Foundation`
   - **Identifier Code**: e.g., `HOPE-IN`
   - **Admin Username**: e.g., `hope_admin`
   - **Password**: e.g., `SecurePass123!`
3. Click **Register & Open Dashboard**.
4. You are immediately logged in to a clean, isolated workspace for your new organization.

---

## 5. Security & Isolation Tests

A comprehensive automated test suite validates multi-tenant security:
- **Multi-Tenant Isolation**: Verified that Organization A users cannot view Organization B campaigns, donors, or donations.
- **URL Parameter Tampering Attack Tests**: Verified that attempting to access `/campaigns/<id>/` or delete records across organization boundaries returns **403 Forbidden**.
- **Cross-Organization Form Injection**: Verified that donations cannot cross-link donors or campaigns from other organizations.
- **Role Restrictions**: Verified that Staff accounts cannot delete campaigns or access member administration.
- **Public vs. Private Data Separation**: Verified that the public homepage does not expose private donor data.

### Run the Test Suite:
```powershell
.\qfund_env\Scripts\python manage.py test tracker
```
**Output**: `Ran 11 tests in 36s ... OK` (11 passed, 0 failed).

---

## 6. Known Limitations & Future Work
- **AWS Deployment**: AWS EC2, RDS, S3, and SNS integrations are scheduled for Phase 2.
- **Live Payment Gateway**: Transactions currently log receipt references; live payment gateways (e.g. Razorpay, Stripe) will be added in Phase 2.
- **Email Delivery**: Standard console email backend is configured; production SMTP or AWS SES will be wired during cloud rollout.
