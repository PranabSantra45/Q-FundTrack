
cd ~/Q-FundTrack

cat > README.md <<'EOF'
# Q-FundTrack: Donation and Campaign Management System

Q-FundTrack is a Django-based platform designed to help nonprofit organizations manage fundraising campaigns, donors, and donation records. It supports multiple organizations with role-based access control and organization-scoped data.

## 1. Features

- Multi-organization workspaces.
- Organization-scoped campaigns, donors, and donations.
- Role-based access control for organization administrators, finance users, and staff.
- Organization registration and onboarding.
- Public homepage for showcasing campaigns.
- Django administration.
- Automated tests for organization isolation and access restrictions.

## 2. Technology Stack

- Python and Django
- HTML, CSS, Bootstrap, and JavaScript
- Django ORM
- SQLite database in the current deployment
- Gunicorn application server
- Amazon EC2 for application hosting
- systemd for managing the application service

## 3. AWS Deployment Status

### Implemented

- **Amazon EC2:** Hosts the Django application.
- **Gunicorn:** Serves the Django WSGI application.
- **systemd:** Manages the `qfundtrack.service` application service.
- **Environment-based configuration:** The Django secret key is loaded from environment variables rather than hardcoded in the settings file.
- **SQLite:** The current deployment uses SQLite for database storage.

### Planned or not yet verified

- **Amazon RDS:** Managed PostgreSQL database migration.
- **Amazon S3:** Cloud storage for campaign images and receipts.
- **Amazon SNS:** Notification delivery integration.
- **Nginx and HTTPS:** Reverse proxy and TLS configuration, if not yet configured.

These services must not be considered implemented until their integrations have been configured and tested.

## 4. Run Locally on Windows

Open PowerShell in the project directory:

```powershell
cd "C:\Users\Pranab Santra\Desktop\Projects\Qu-FundMe -- AWS Cloud"
```

Activate the existing virtual environment or use its Python executable:

```powershell
.\qfund_env\Scripts\python.exe -m pip install -r requirements.txt
.\qfund_env\Scripts\python.exe manage.py migrate
.\qfund_env\Scripts\python.exe manage.py runserver
```

Open the application at:

- Homepage: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Organization registration: http://127.0.0.1:8000/register/
- Django administration: http://127.0.0.1:8000/admin/

## 5. Deploy on Amazon EC2

The current EC2 deployment uses Gunicorn and the `qfundtrack.service` systemd service.

General deployment workflow:

1. Provision an EC2 instance and install a compatible Python version.
2. Clone the repository and create a virtual environment.
3. Install application dependencies.
4. Configure environment variables securely outside the repository.
5. Run database migrations.
6. Configure allowed hosts and production Django settings.
7. Configure and start Gunicorn using systemd.
8. Configure network access, a domain, HTTPS, and a reverse proxy as required.
9. Verify the application and review server logs.

The actual server paths, environment-file location, security-group rules, and service configuration depend on the deployment environment. Never publish private keys, credentials, or production environment files.

Useful service commands on the configured EC2 instance:

```bash
sudo systemctl status qfundtrack.service --no-pager
sudo systemctl restart qfundtrack.service
sudo journalctl -u qfundtrack.service -n 100 --no-pager
```

## 6. Configuration and Security

- Keep `SECRET_KEY` and other credentials in environment variables or a secure secrets manager.
- Keep `DEBUG` disabled in production.
- Configure `ALLOWED_HOSTS` for the actual deployment hostname or IP.
- Do not commit `.env` files, database backups, private keys, virtual environments, or real donor data.
- Change any default or demonstration passwords before deployment.
- Use HTTPS and appropriate access controls for production use.
- Review tenant isolation, authorization, database backups, and logging before handling real donor information.

## 7. Testing

Run the Django application tests:

```bash
python manage.py test tracker
```

The test suite should be run in the current environment before reporting test results. Tests for tenant isolation and role restrictions are important, but passing tests alone do not guarantee production security.

## 8. Limitations and Future Enhancements

- Migration from SQLite to Amazon RDS PostgreSQL.
- Integration with Amazon S3 for uploaded documents.
- Integration with Amazon SNS or another notification provider.
- Production email delivery configuration.
- Payment gateway integration.
- Additional deployment hardening, monitoring, backups, and HTTPS configuration.

## 9. Project Repository

GitHub: https://github.com/PranabSantra45/Q-FundTrack
EOF

cd ~/Q-FundTrack

cat > README.md <<'EOF'
# Q-FundTrack: Donation and Campaign Management System

Q-FundTrack is a Django-based platform designed to help nonprofit organizations manage fundraising campaigns, donors, and donation records. It supports multiple organizations with role-based access control and organization-scoped data.

## 1. Features

- Multi-organization workspaces.
- Organization-scoped campaigns, donors, and donations.
- Role-based access control for organization administrators, finance users, and staff.
- Organization registration and onboarding.
- Public homepage for showcasing campaigns.
- Django administration.
- Automated tests for organization isolation and access restrictions.

## 2. Technology Stack

- Python and Django
- HTML, CSS, Bootstrap, and JavaScript
- Django ORM
- SQLite database in the current deployment
- Gunicorn application server
- Amazon EC2 for application hosting
- systemd for managing the application service

## 3. AWS Deployment Status

### Implemented

- **Amazon EC2:** Hosts the Django application.
- **Gunicorn:** Serves the Django WSGI application.
- **systemd:** Manages the `qfundtrack.service` application service.
- **Environment-based configuration:** The Django secret key is loaded from environment variables rather than hardcoded in the settings file.
- **SQLite:** The current deployment uses SQLite for database storage.

### Planned or not yet verified

- **Amazon RDS:** Managed PostgreSQL database migration.
- **Amazon S3:** Cloud storage for campaign images and receipts.
- **Amazon SNS:** Notification delivery integration.
- **Nginx and HTTPS:** Reverse proxy and TLS configuration, if not yet configured.

These services must not be considered implemented until their integrations have been configured and tested.

## 4. Run Locally on Windows

Open PowerShell in the project directory:

```powershell
cd "C:\Users\Pranab Santra\Desktop\Projects\Qu-FundMe -- AWS Cloud"
```

Activate the existing virtual environment or use its Python executable:

```powershell
.\qfund_env\Scripts\python.exe -m pip install -r requirements.txt
.\qfund_env\Scripts\python.exe manage.py migrate
.\qfund_env\Scripts\python.exe manage.py runserver
```

Open the application at:

- Homepage: http://127.0.0.1:8000/
- Login: http://127.0.0.1:8000/login/
- Organization registration: http://127.0.0.1:8000/register/
- Django administration: http://127.0.0.1:8000/admin/

## 5. Deploy on Amazon EC2

The current EC2 deployment uses Gunicorn and the `qfundtrack.service` systemd service.

General deployment workflow:

1. Provision an EC2 instance and install a compatible Python version.
2. Clone the repository and create a virtual environment.
3. Install application dependencies.
4. Configure environment variables securely outside the repository.
5. Run database migrations.
6. Configure allowed hosts and production Django settings.
7. Configure and start Gunicorn using systemd.
8. Configure network access, a domain, HTTPS, and a reverse proxy as required.
9. Verify the application and review server logs.

The actual server paths, environment-file location, security-group rules, and service configuration depend on the deployment environment. Never publish private keys, credentials, or production environment files.

Useful service commands on the configured EC2 instance:

```bash
sudo systemctl status qfundtrack.service --no-pager
sudo systemctl restart qfundtrack.service
sudo journalctl -u qfundtrack.service -n 100 --no-pager
```

## 6. Configuration and Security

- Keep `SECRET_KEY` and other credentials in environment variables or a secure secrets manager.
- Keep `DEBUG` disabled in production.
- Configure `ALLOWED_HOSTS` for the actual deployment hostname or IP.
- Do not commit `.env` files, database backups, private keys, virtual environments, or real donor data.
- Change any default or demonstration passwords before deployment.
- Use HTTPS and appropriate access controls for production use.
- Review tenant isolation, authorization, database backups, and logging before handling real donor information.

## 7. Testing

Run the Django application tests:

```bash
python manage.py test tracker
```

The test suite should be run in the current environment before reporting test results. Tests for tenant isolation and role restrictions are important, but passing tests alone do not guarantee production security.

## 8. Limitations and Future Enhancements

- Migration from SQLite to Amazon RDS PostgreSQL.
- Integration with Amazon S3 for uploaded documents.
- Integration with Amazon SNS or another notification provider.
- Production email delivery configuration.
- Payment gateway integration.
- Additional deployment hardening, monitoring, backups, and HTTPS configuration.

## 9. Project Repository

GitHub: https://github.com/PranabSantra45/Q-FundTrack
EOF
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
