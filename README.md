
# Q-FundTrack
### Multi-Organization Donation and Campaign Management System

Q-FundTrack is a cloud-hosted web application designed to help nonprofit organizations manage fundraising campaigns, donor information, and donation records through a centralized platform.

The application is developed using **Python and Django** and deployed on **Amazon EC2**. It supports a multi-organization structure, allowing different organizations to manage their campaigns, donors, and donations within the same application.

The current deployment uses **Amazon EC2, Gunicorn, systemd, and SQLite**. Integration with additional AWS services such as Amazon RDS, Amazon S3, and Amazon SNS is planned for future development.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [Application Architecture](#application-architecture)
- [Multi-Organization Architecture](#multi-organization-architecture)
- [AWS Deployment](#aws-deployment)
- [AWS Deployment Screenshots](#aws-deployment-screenshots)
- [Local Installation and Setup](#local-installation-and-setup)
- [EC2 Deployment Management](#ec2-deployment-management)
- [Configuration and Security](#configuration-and-security)
- [Testing](#testing)
- [Limitations and Future Enhancements](#limitations-and-future-enhancements)
- [Project Structure](#project-structure)
- [Repository](#repository)

---

## Project Overview

Nonprofit organizations regularly manage fundraising campaigns, donor information, and donation records. Maintaining these records manually or across multiple spreadsheets can make it difficult to organize information, monitor fundraising progress, and maintain consistency.

Q-FundTrack addresses this problem by providing a centralized donation and campaign management platform.

The application enables organizations to:

- Create and manage fundraising campaigns.
- Maintain donor information.
- Record and track donations.
- Associate campaigns, donors, and donations with their respective organizations.
- Monitor fundraising targets and campaign progress.
- Manage users with different responsibilities.
- Access fundraising information through a centralized web application.

The system follows a multi-organization architecture, allowing multiple nonprofit organizations to use the same platform while maintaining organization-specific records.

## Key Features

### 1. Campaign Management
- Create and manage fundraising campaigns.
- Maintain campaign descriptions and details.
- Define fundraising targets.
- Associate campaigns with specific organizations.
- Monitor campaign progress based on recorded donations.

### 2. Donor Management
- Register and maintain donor information.
- Organize donor records by organization.
- Maintain donor details for fundraising activities.

### 3. Donation Management
- Record donations against fundraising campaigns.
- Maintain donation details and receipt references.
- Associate donations with the relevant organization.
- Track donation records for campaign monitoring.

### 4. Multi-Organization Support
- Centralized organization management.
- Organization-based user profiles.
- Organization associations for campaigns, donors, and donations.
- Organization-scoped data handling.

### 5. User Roles and Access Management

The application includes role-oriented access for different responsibilities:

| Role | Responsibility |
|---|---|
| Admin | Administrative and management operations |
| Finance | Donation and financial record management |
| Staff | Day-to-day campaign and donor operations |

### 6. User Registration and Authentication
- User registration.
- Login and authentication.
- User profile management.
- Organization-related onboarding structure.

### 7. Public and Administrative Interfaces
- Public-facing homepage.
- User login and registration pages.
- Django administration interface.
- Application management through authenticated access.

---

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Backend Framework | Django |
| Frontend | HTML, CSS, Bootstrap, JavaScript |
| Database Access | Django ORM |
| Current Database | SQLite |
| Application Server | Gunicorn |
| Cloud Platform | Amazon Web Services (AWS) |
| Cloud Hosting | Amazon EC2 |
| Operating System | Amazon Linux 2023 |
| Process Management | systemd |
| Version Control | Git and GitHub |

### AWS Services

| AWS Service | Status | Purpose |
|---|---|---|
| Amazon EC2 | Implemented | Hosting the Django application |
| Gunicorn | Implemented | Running the Django application |
| systemd | Implemented | Managing the application service |
| SQLite | Currently used | Application database |
| Amazon RDS | Planned | Managed relational database, preferably PostgreSQL |
| Amazon S3 | Planned | File and document storage |
| Amazon SNS | Planned | Notification services |
| Nginx | Planned | Reverse proxy and web server |
| HTTPS / SSL | Planned | Secure communication |

---

## Application Architecture

### Current Architecture

The current application follows this request flow:

1. The user accesses the application through a web browser.
2. The request reaches the Amazon EC2 instance.
3. Gunicorn receives the request and forwards it to Django.
4. Django processes the request and executes the application logic.
5. Django ORM communicates with the SQLite database.
6. The response is returned to the user's browser.

```text
             User Browser
                  |
                  |
             HTTP Request
                  |
                  v
          Amazon EC2 Instance
          (Amazon Linux 2023)
                  |
                  v
             Gunicorn
          (WSGI Application)
                  |
                  v
           Django Framework
                  |
                  v
             SQLite DB
```

### Planned Future Architecture

```text
              User Browser
                   |
                   v
              HTTPS / SSL
                   |
                   v
                 Nginx
                   |
                   v
              Amazon EC2
                   |
                   v
             Gunicorn + Django
                   |
          +--------+--------+
          |        |        |
          v        v        v
        Amazon   Amazon   Amazon
         RDS      S3       SNS
      (Database)(Storage)(Notifications)
```

**Note:** The second architecture represents the intended future infrastructure. These additional AWS integrations are not yet verified as implemented.

---

## Multi-Organization Architecture

Q-FundTrack follows an organization-based data model.

The main components include:

| Model | Purpose |
|---|---|
| Organization | Stores organization information |
| UserProfile | Associates user accounts with organizations |
| Campaign | Stores fundraising campaign records |
| Donor | Stores donor information |
| Donation | Stores donation records |

Campaign, Donor, and Donation records are associated with organizations through organization relationships.

A database migration was introduced to support the multi-organization structure and assign existing records to a default organization where applicable.

**Default Organization**

- Organization Name: `Global FundTrack NGO`
- Organization Code: `DEFAULT-ORG`

Organization-level data isolation must be enforced through application queries and authorization checks. Database relationships alone do not guarantee tenant isolation.

---

## AWS Deployment

### Deployment Environment

| Configuration | Details |
|---|---|
| Cloud Provider | AWS |
| Service | Amazon EC2 |
| Operating System | Amazon Linux 2023 |
| Application Directory | `/home/ec2-user/Q-FundTrack` |
| Linux User | `ec2-user` |
| Python Environment | `.venv` |
| Application Framework | Django |
| Application Server | Gunicorn |
| Process Manager | systemd |
| Service Name | `qfundtrack.service` |
| Application Port | `8000` |
| Database | SQLite |

### Implemented Deployment Components

The application has been deployed to an Amazon EC2 instance.

The deployment includes:

- EC2 instance provisioning.
- Amazon Linux 2023 environment.
- Python virtual environment setup.
- Django dependency installation.
- Database migrations.
- Gunicorn application server configuration.
- systemd service configuration.
- Environment-based Django secret key configuration.
- Production configuration with `DEBUG = False`.
- Application hosting on port `8000`.
- Elastic IP association for a stable public IPv4 address.

The Gunicorn service is managed using systemd, allowing the application process to be started, stopped, restarted, and monitored through Linux service management commands.

### Application Service

The systemd service is named:

```bash
qfundtrack.service
```

The application is configured to run using Gunicorn:

```bash
gunicorn --workers 2 --bind 0.0.0.0:8000 qfundtrack.wsgi:application
```

### Deployment Verification

The following commands were used to verify the application deployment.

**Check application service:**

```bash
sudo systemctl status qfundtrack.service --no-pager
```

**Check Gunicorn listening port:**

```bash
sudo ss -lntp | grep ':8000'
```

**Test application response locally on EC2:**

```bash
curl -I --max-time 10 http://127.0.0.1:8000/
```

A successful HTTP response confirms that the application is responding locally on the EC2 instance.

Public browser access also depends on the EC2 security group, Django `ALLOWED_HOSTS`, and the configured public IP address or domain.

---

## Local Installation and Setup

### Prerequisites

- Python 3.x
- Git
- pip
- Windows, Linux, or macOS

### 1. Clone the Repository

```bash
git clone https://github.com/PranabSantra45/Q-FundTrack.git
```

Navigate into the project directory:

```bash
cd Q-FundTrack
```

### 2. Create a Virtual Environment

For Windows PowerShell:

```powershell
python -m venv qfund_env
```

Activate it:

```powershell
.\qfund_env\Scripts\Activate.ps1
```

For Linux or macOS:

```bash
python3 -m venv qfund_env
source qfund_env/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

Open the following URLs in your browser:

| Page | URL |
|---|---|
| Homepage | http://15.135.13.178:8000/ |
| Login | http://15.135.13.178:8000/login/ |
| Registration | http://15.135.13.178:8000/register/ |
| Django Admin | http://15.135.13.178:8000/admin/ |

The Django development server is intended for local development and testing. The EC2 deployment uses Gunicorn managed through systemd.

---

## EC2 Deployment Management

The following commands are used to manage the deployed application.

### Navigate to the Application Directory

```bash
cd /home/ec2-user/Q-FundTrack
```

### Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### Pull Latest Changes from GitHub

```bash
git pull origin main
```

### Install Updated Dependencies

```bash
pip install -r requirements.txt
```

### Apply Database Migrations

```bash
python manage.py migrate
```

### Restart the Application

```bash
sudo systemctl restart qfundtrack.service
```

### Check Application Status

```bash
sudo systemctl status qfundtrack.service --no-pager
```

### View Application Logs

```bash
sudo journalctl -u qfundtrack.service -n 50 --no-pager
```

### Test the Application

```bash
curl -I --max-time 10 http://127.0.0.1:8000/
```

---

## Configuration and Security

The application uses production-oriented Django configuration.

### Important Configuration

- `DEBUG = False` for the EC2 deployment.
- `SECRET_KEY` is loaded using an environment variable.
- `ALLOWED_HOSTS` is configured for permitted application hosts.
- The EC2 security group controls inbound network access.
- Application configuration and sensitive credentials are kept outside the Git repository.

### Environment Configuration

The EC2 deployment uses an environment file stored outside the project directory:

```text
/home/ec2-user/.qfundtrack.env
```

This file contains sensitive configuration and must never be committed to GitHub.

### Security Recommendations

Before using the application with real organizations and donor information:

- Use strong administrator passwords.
- Remove or change development credentials.
- Review user roles and permissions.
- Verify organization-level data isolation.
- Restrict EC2 security group access.
- Configure HTTPS/SSL.
- Configure regular database backups.
- Protect uploaded files and sensitive information.
- Review application logs for accidental exposure of confidential data.

---

## Testing

The tracker application can be tested using Django's test framework.

Run:

```bash
python manage.py test tracker
```

A previous test execution reported:

```text
Ran 11 tests
OK
```

This is a historical test result. Run the test suite again after code changes to verify the current version.

---

## Limitations and Future Enhancements

The following improvements are planned for future development:

| Feature | Current Status | Future Enhancement |
|---|---|---|
| Cloud Hosting | EC2 deployed | Improve production infrastructure |
| Database | SQLite | Migrate to Amazon RDS PostgreSQL |
| File Storage | Local/application storage | Integrate Amazon S3 |
| Notifications | Not yet integrated with SNS | Integrate Amazon SNS |
| Web Server | Gunicorn | Add Nginx reverse proxy |
| HTTPS | Not yet verified | Configure SSL/TLS |
| Payment Gateway | Receipt references maintained | Integrate Razorpay or Stripe |
| Email Delivery | Development console backend | Configure SMTP or Amazon SES |
| Monitoring | Basic service logs | Add monitoring and alerting |
| Backup | Not yet fully configured | Implement automated backups |

### Future Development Goals

1. Migrate the database from SQLite to Amazon RDS.
2. Integrate Amazon S3 for campaign banners, uploaded documents, and donation receipts.
3. Integrate Amazon SNS for notifications.
4. Configure Nginx and HTTPS for production access.
5. Implement live payment gateway integration.
6. Configure production email delivery.
7. Improve monitoring, logging, and backup mechanisms.
8. Perform additional security testing and authorization reviews.

---

## Project Structure

```text
Q-FundTrack/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── qfundtrack/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tracker/
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── ...
│
└── docs/
    └── aws-screenshots/
```

The structure represents the main Django project, application, and documentation directories. Additional files and folders may be present as development continues.

---

## Repository

**Project Name:** Q-FundTrack  
**Project Type:** Nonprofit Donation and Campaign Management System  
**Backend:** Python, Django  
**Frontend:** HTML, CSS, Bootstrap, JavaScript  
**Cloud Platform:** Amazon Web Services  
**Current Hosting:** Amazon EC2  
**Current Database:** SQLite  

### GitHub Repository

[PranabSantra45/Q-FundTrack](https://github.com/PranabSantra45/Q-FundTrack)

---

<p align="center">
  <b>Q-FundTrack</b><br>
  Simplifying Donation and Campaign Management for Nonprofit Organizations.
</p>
