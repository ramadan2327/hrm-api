# HRM API — Limkokwing University Sierra Leone

![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Python](https://img.shields.io/badge/Python-3.14-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

A production-grade **Human Resource Management REST API** built with FastAPI and PostgreSQL.
Developed for **PROG315 — Object-Oriented Programming 2** at Limkokwing University of Creative Technology, Sierra Leone.

---

## SDG Alignment

This project supports **SDG 8 — Decent Work and Economic Growth** by providing digital infrastructure for:
- Managing fair and transparent employment records
- Tracking attendance and leave for workforce accountability
- Delivering structured payroll management in Sierra Leone

---

## Features

- JWT Authentication with Role-Based Access Control (Admin, Manager, Employee)
- Employee lifecycle management (create, update, deactivate)
- Department management with employee assignment
- Attendance tracking with clock in and clock out
- Leave request and approval workflow
- Payroll and salary history management
- Performance review system
- Dashboard summary endpoint
- Auto-generated Swagger UI and ReDoc documentation

---

## Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Pydantic | Data validation |
| JWT + OAuth2 | Authentication |
| bcrypt | Password hashing |
| Uvicorn | ASGI server |
| Alembic | Database migrations |

---

## Project Structure

hrm_api/
├── app/
│   ├── main.py           # App entry point
│   ├── database.py       # Database connection
│   ├── config.py         # Environment settings
│   ├── auth.py           # JWT and password logic
│   ├── dependencies.py   # Dependency injection
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   └── routers/          # API endpoints
├── seed.py               # Database seeder
├── .env.example          # Environment template
├── requirements.txt      # Dependencies
└── README.md

---

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/ramadan2327/hrm-api.git
cd hrm_api
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```
Edit `.env` with your PostgreSQL credentials.

### 5. Create the database
Open pgAdmin and create a database called `hrm_db`.

### 6. Run the seed script
```bash
python seed.py
```

### 7. Start the server
```bash
uvicorn app.main:app --reload
```

---

## API Documentation

| URL | Description |
|---|---|
| http://127.0.0.1:8000/docs | Swagger UI |
| http://127.0.0.1:8000/redoc | ReDoc |
| http://127.0.0.1:8000/health | Health check |

---

## Default Credentials

| Role | Email | Password |
|---|---|---|
| Admin    | ramadan@limkokwing.edu.sl | Admin1234    |
| Manager  | kesuma@limkokwing.edu.sl  | Manager1234  |
| Employee | dwight@limkokwing.edu.sl  | Employee1234 |
---

## API Endpoints

### Auth
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/v1/auth/register | Register user | Public |
| POST | /api/v1/auth/login | Login | Public |

### Employees
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /api/v1/employees/ | List employees | Admin, Manager |
| POST | /api/v1/employees/ | Create employee | Admin |
| GET | /api/v1/employees/{id} | Get employee | All |
| PUT | /api/v1/employees/{id} | Update employee | Admin, Manager |
| PATCH | /api/v1/employees/{id}/deactivate | Deactivate | Admin |
| GET | /api/v1/employees/dashboard/summary | Dashboard | Admin, Manager |

### Departments
| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | /api/v1/departments/ | List departments | Admin, Manager |
| POST | /api/v1/departments/ | Create department | Admin |
| GET | /api/v1/departments/{id} | Get department | Admin, Manager |
| PUT | /api/v1/departments/{id} | Update department | Admin |
| DELETE | /api/v1/departments/{id} | Delete department | Admin |

### Attendance
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/v1/attendance/clock-in | Clock in | All |
| POST | /api/v1/attendance/clock-out | Clock out | All |
| GET | /api/v1/attendance/ | List records | All |

### Leave
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/v1/leave/request | Submit request | All |
| GET | /api/v1/leave/ | List requests | All |
| PATCH | /api/v1/leave/{id}/action | Approve/Reject | Admin, Manager |

### Payroll
| Method | Endpoint | Description | Access |
|---|---|---|---|
| PUT | /api/v1/payroll/{id}/salary | Set salary | Admin |
| GET | /api/v1/payroll/summary | Pay summary | Admin |
| GET | /api/v1/payroll/{id}/history | Salary history | Admin |

### Performance Reviews
| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | /api/v1/performance/ | Create review | Admin, Manager |
| GET | /api/v1/performance/ | List reviews | All |
| GET | /api/v1/performance/{id} | Get review | All |
| DELETE | /api/v1/performance/{id} | Delete review | Admin |

---

## License

MIT License — see LICENSE file for details.

---

## Authors
## Group Members

| Name | Role |
|---|---|
| Ramadan Kamara | Backend Developer & Project Lead |
| Alhaji Kesuma Kamara | Database & Authentication |
| Dwight Doherty | API Design & Documentation |

PROG315 — Object Oriented Programming 2
Limkokwing University of Creative Technology, Sierra Leone
Semester 4 — March 2026 to July 2026