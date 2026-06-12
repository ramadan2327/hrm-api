from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.models import Employee, Department, Attendance, LeaveRequest, Salary, PerformanceReview
from app.routers import auth, employees, departments, attendance, leave, payroll, performance

# ── Create all tables ─────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── App instance ──────────────────────────────────────────────────────
app = FastAPI(
    title="HRM API — Limkokwing University Sierra Leone",
    description="""
## Human Resource Management API

Built for **PROG315 Object-Oriented Programming 2** at Limkokwing University.

### Features
- JWT Authentication and Role-Based Access Control
- Employee lifecycle management
- Department management
- Attendance tracking with clock in and clock out
- Leave request and approval workflow
- Payroll management
- Performance reviews

### SDG Alignment
This API supports **SDG 8 — Decent Work and Economic Growth** by providing
digital infrastructure for managing fair employment, transparent payroll,
and structured workforce development in Sierra Leone.

### Roles
- **Admin** — Full access to all endpoints
- **Manager** — Can view employees, approve leave, manage attendance
- **Employee** — Can view own profile, own attendance, own leave
    """,
    version="1.0.0",
    contact={
        "name": "Limkokwing University Sierra Leone",
        "email": "amandus.bcoker@limkokwing.edu.sl"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
)

# ── CORS Middleware ───────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Include Routers ───────────────────────────────────────────────────
app.include_router(auth.router,         prefix="/api/v1")
app.include_router(employees.router,    prefix="/api/v1")
app.include_router(departments.router,  prefix="/api/v1")
app.include_router(attendance.router,   prefix="/api/v1")
app.include_router(leave.router,        prefix="/api/v1")
app.include_router(payroll.router,      prefix="/api/v1")
app.include_router(performance.router,  prefix="/api/v1")


# ── Health Check ──────────────────────────────────────────────────────
@app.get("/health", tags=["Health"])
def health():   
    return {
        "status": "ok",
        "version": "1.0.0",
        "project": "HRM API",
        "university": "Limkokwing University Sierra Leone"
    }