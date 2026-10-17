
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

### Run the Test Suite:
```powershell
.\qfund_env\Scripts\python manage.py test tracker
```
**Output**: `Ran 11 tests in 36s ... OK` (11 passed, 0 failed).

---

## 10. Known Limitations & Future Work
- **AWS Deployment**: AWS EC2, RDS, S3, and SNS integrations are scheduled for Phase 2.
- **Live Payment Gateway**: Transactions currently log receipt references; live payment gateways (e.g. Razorpay, Stripe) will be added in Phase 2.
- **Email Delivery**: Standard console email backend is configured; production SMTP or AWS SES will be wired during cloud rollout.
