# 🏥 Hospital ERM

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-15%20passing-brightgreen.svg)](#)

**Enterprise-grade Hospital Management System** — connects doctors, patients, and staff in one platform.

---

## Overview

Hospital ERM is a modular Django-based platform with clean architecture, REST API, and a modern responsive UI.

| Module | Status | Description |
|--------|--------|-------------|
| Auth & Roles | ✅ | Doctor/Patient registration, login, password reset |
| Appointments | ✅ | Book, filter, accept/wait/cancel workflow |
| Blog CMS | ✅ | Create, publish, draft, comment, categories |
| Dashboards | ✅ | Real-time stats, charts, upcoming appointments |
| Profile | ✅ | Personal info, avatar, password change, address |
| REST API | ✅ | 14 endpoints (CRUD) via Django REST Framework |
| EMR | ✅ | Medical records, vitals, prescriptions, lab orders |
| Audit Log | ✅ | Automatic tracking of all system actions |
| Docker | ✅ | Containerized with PostgreSQL + Nginx |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Django 4.2 |
| Frontend | Bootstrap 5, Bootstrap Icons, Chart.js |
| API | Django REST Framework |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Infrastructure | Docker, Nginx, Gunicorn, WhiteNoise |

---

## Quick Start

```bash
git clone <repo> && cd hospital-erm
python -m venv venv && source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # edit with your settings
python manage.py migrate
python manage.py loaddata seed/*.json
python manage.py runserver
```

Visit **http://127.0.0.1:8000**

---

## Docker

```bash
docker-compose up --build -d
```

---

## API Endpoints (`/api/`)

| Endpoint | Description |
|----------|-------------|
| `users/` | User management |
| `doctors/` | Doctor profiles |
| `patients/` | Patient profiles |
| `specialties/` | Medical specialties |
| `appointments/` | Appointment CRUD |
| `blogs/` | Published blogs |
| `categories/` | Blog categories |
| `comments/` | Blog comments |
| `medical-records/` | Patient medical records |
| `vital-signs/` | Vital signs |
| `prescriptions/` | Prescriptions |
| `lab-orders/` | Laboratory orders |

---

## Project Structure

```
hospital_erm/
├── hospital/          Django project config
├── users/             Auth, profiles, roles
├── doctors/           Doctor features
├── patients/          Patient features
├── core/              Constants, services, middleware, signals
├── emr/               Electronic Medical Records
├── templates/         HTML templates
├── static/            CSS, JS, images
├── seed/              Database fixtures
├── Dockerfile
├── docker-compose.yml
└── nginx.conf
```

---

## Architecture Highlights

- **Service Layer** — Business logic separated from views (`core/services.py`)
- **Enums** — Magic strings eliminated (`core/constants.py`)
- **Optimized Queries** — `select_related` on all foreign keys
- **Django Forms** — Validation on all inputs
- **Error Handling** — `try/except` with user-friendly messages
- **Security** — Env-based config, HSTS, CSRF, SSL-ready
- **Tests** — 15 passing tests across all apps

---

## License

MIT — see [LICENSE](LICENSE)
