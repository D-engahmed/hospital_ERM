# 🏥 Hospital ERM (Enterprise Resource Management)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Enterprise-grade Hospital Management System** — A comprehensive platform connecting doctors, patients, and administrative staff.

---

## 📋 Overview

Hospital ERM is a full-featured hospital management system built with Django. It streamlines appointment scheduling, patient records, doctor-patient communication, and administrative workflows.

### نظام إدارة المستشفيات
نظام متكامل لإدارة المستشفيات والعيادات يربط بين الأطباء والمرضى والإدارة.

---

## ✨ Features

### ✅ Implemented
| Module | Description |
|--------|-------------|
| **User Management** | Registration, authentication, role-based access (Doctor/Patient) |
| **Appointment System** | Book, manage, filter, and track appointments with status workflow |
| **Blog CMS** | Doctors create, publish, and manage medical blogs with categories |
| **Patient Portal** | Dashboard with appointments overview and profile management |
| **Doctor Portal** | Dashboard with statistics, charts, and appointment management |
| **Profile Management** | Personal info, avatar, password change, address management |
| **Password Reset** | Forgot password flow with email token |
| **REST API** | Full RESTful API via Django REST Framework |

### 🚧 Planned
- **EMR (Electronic Medical Records)** — Patient clinical records, vitals, prescriptions
- **Lab Orders** — Test ordering and results
- **Billing & Invoicing** — Revenue cycle management
- **Notifications** — Real-time alerts and reminders

---

## 🛠️ Tech Stack

| Tier | Technology |
|------|------------|
| **Backend** | Python 3.11+, Django 4.2 |
| **Frontend** | HTML5, CSS3, Bootstrap 5, jQuery, Chart.js |
| **API** | Django REST Framework |
| **Database** | SQLite (dev) / PostgreSQL (production) |
| **Static Files** | WhiteNoise |
| **Server** | Gunicorn + Nginx |
| **Container** | Docker & Docker Compose |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-org/hospital-erm.git
cd hospital-erm

# 2. Create virtual environment
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your settings

# 5. Run migrations
python manage.py migrate

# 6. Load seed data
python manage.py loaddata seed/categories.json
python manage.py loaddata seed/specialities.json
python manage.py loaddata seed/status.json
python manage.py loaddata seed/time.json

# 7. Start development server
python manage.py runserver
```

Visit **http://127.0.0.1:8000** to access the application.

---

## 🐳 Docker Deployment

```bash
docker-compose up --build -d
```

The application will be available at **http://localhost**.

---

## 📚 API Documentation

The REST API is available at `/api/` with the following endpoints:

| Endpoint | Description |
|----------|-------------|
| `/api/users/` | User management |
| `/api/doctors/` | Doctor profiles |
| `/api/patients/` | Patient profiles |
| `/api/specialties/` | Medical specialties |
| `/api/appointments/` | Appointment management |
| `/api/blogs/` | Published blogs |
| `/api/categories/` | Blog categories |
| `/api/comments/` | Blog comments |
| `/api/medical-records/` | Patient medical records |
| `/api/vital-signs/` | Vital signs |
| `/api/prescriptions/` | Prescriptions |
| `/api/lab-orders/` | Laboratory orders |

API authentication via session or basic auth.

---

## 📁 Project Structure

```
hospital_erm/
├── hospital/          # Django project configuration
├── users/             # User management (auth, profiles, roles)
├── doctors/           # Doctor features (blogs, appointments)
├── patients/          # Patient features (booking, dashboard)
├── core/              # Shared services (audit logging)
├── emr/               # Electronic Medical Records
├── templates/         # HTML templates
├── static/            # Static assets (CSS, JS, images)
├── media/             # User uploaded files
├── seed/              # Database seed data
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

---

## 🔒 Security

- Environment-based configuration (`.env`)
- CSRF protection
- Session-based authentication
- Password validation & hashing
- SSL/HTTPS ready
- Security headers (HSTS, XSS, Content-Type)
- Rate limiting ready (django-axes)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

## 🤝 Support

For enterprise support, customization, or deployment assistance, please contact the development team.
