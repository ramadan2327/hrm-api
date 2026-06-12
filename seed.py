"""
Seed script — run once to populate the database with sample data.
Usage: python seed.py
"""

from app.database import SessionLocal, engine, Base
from app.models.employee import Employee, RoleEnum, StatusEnum
from app.models.department import Department
from app.models.attendance import Attendance
from app.models.leave import LeaveRequest, LeaveTypeEnum, LeaveStatusEnum
from app.models.payroll import Salary
from app.models.performance import PerformanceReview
from app.auth import hash_password
from datetime import date, datetime, timezone
import sys


def seed():
    db = SessionLocal()
    try:
        # ── Check if already seeded ──────────────────────────────────
        if db.query(Employee).count() > 0:
            print("❌ Database already has data. Clear it first or skip seeding.")
            return

        print("🌱 Seeding database...")

        # ── Departments ───────────────────────────────────────────────
        departments = [
            Department(name="Human Resources",    description="Manages employee welfare and recruitment"),
            Department(name="Engineering",         description="Software development and IT infrastructure"),
            Department(name="Finance",             description="Financial planning and payroll management"),
            Department(name="Marketing",           description="Brand management and customer outreach"),
            Department(name="Operations",          description="Day-to-day business operations"),
        ]
        for dept in departments:
            db.add(dept)
        db.commit()
        print(f"   ✅ {len(departments)} departments created")

        # Fetch departments
        hr_dept  = db.query(Department).filter(Department.name == "Human Resources").first()
        eng_dept = db.query(Department).filter(Department.name == "Engineering").first()
        fin_dept = db.query(Department).filter(Department.name == "Finance").first()
        mkt_dept = db.query(Department).filter(Department.name == "Marketing").first()
        ops_dept = db.query(Department).filter(Department.name == "Operations").first()

        # ── Employees ─────────────────────────────────────────────────
        employees_data = [
            Employee(
                full_name="Admin User",
                email="admin@limkokwing.edu.sl",
                hashed_password=hash_password("Admin1234"),
                phone="+232-76-000001",
                job_title="System Administrator",
                hire_date=date(2022, 1, 10),
                role=RoleEnum.admin,
                status=StatusEnum.active,
                department_id=hr_dept.id
            ),
            Employee(
                full_name="Sarah Manager",
                email="sarah@limkokwing.edu.sl",
                hashed_password=hash_password("Manager1234"),
                phone="+232-76-000002",
                job_title="HR Manager",
                hire_date=date(2022, 3, 15),
                role=RoleEnum.manager,
                status=StatusEnum.active,
                department_id=hr_dept.id
            ),
            Employee(
                full_name="Alice Johnson",
                email="alice@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-000003",
                job_title="Software Engineer",
                hire_date=date(2023, 1, 20),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=eng_dept.id
            ),
            Employee(
                full_name="Bob Smith",
                email="bob@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-000004",
                job_title="Financial Analyst",
                hire_date=date(2023, 4, 10),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=fin_dept.id
            ),
            Employee(
                full_name="Grace Kamara",
                email="grace@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-000005",
                job_title="Marketing Specialist",
                hire_date=date(2023, 6, 1),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=mkt_dept.id
            ),
            Employee(
                full_name="James Conteh",
                email="james@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-000006",
                job_title="Operations Officer",
                hire_date=date(2024, 1, 5),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=ops_dept.id
            ),
        ]
        for emp in employees_data:
            db.add(emp)
        db.commit()
        print(f"   ✅ {len(employees_data)} employees created")

        # Fetch employees
        admin = db.query(Employee).filter(Employee.email == "admin@limkokwing.edu.sl").first()
        sarah = db.query(Employee).filter(Employee.email == "sarah@limkokwing.edu.sl").first()
        alice = db.query(Employee).filter(Employee.email == "alice@limkokwing.edu.sl").first()
        bob   = db.query(Employee).filter(Employee.email == "bob@limkokwing.edu.sl").first()
        grace = db.query(Employee).filter(Employee.email == "grace@limkokwing.edu.sl").first()
        james = db.query(Employee).filter(Employee.email == "james@limkokwing.edu.sl").first()

        # ── Salaries ──────────────────────────────────────────────────
        salaries = [
            Salary(employee_id=admin.id,  amount=120000, currency="SLL", effective_date=date(2022, 1, 10)),
            Salary(employee_id=sarah.id,  amount=95000,  currency="SLL", effective_date=date(2022, 3, 15)),
            Salary(employee_id=alice.id,  amount=85000,  currency="SLL", effective_date=date(2023, 1, 20)),
            Salary(employee_id=bob.id,    amount=80000,  currency="SLL", effective_date=date(2023, 4, 10)),
            Salary(employee_id=grace.id,  amount=75000,  currency="SLL", effective_date=date(2023, 6,  1)),
            Salary(employee_id=james.id,  amount=70000,  currency="SLL", effective_date=date(2024, 1,  5)),
        ]
        for salary in salaries:
            db.add(salary)
        db.commit()
        print(f"   ✅ {len(salaries)} salary records created")

        # ── Attendance ────────────────────────────────────────────────
        attendances = [
            Attendance(
                employee_id=alice.id,
                date=date.today(),
                clock_in=datetime.now(timezone.utc),
                status="open"
            ),
            Attendance(
                employee_id=bob.id,
                date=date.today(),
                clock_in=datetime.now(timezone.utc),
                clock_out=datetime.now(timezone.utc),
                hours_worked=8.0,
                status="closed"
            ),
        ]
        for att in attendances:
            db.add(att)
        db.commit()
        print(f"   ✅ {len(attendances)} attendance records created")

        # ── Leave Requests ────────────────────────────────────────────
        leaves = [
            LeaveRequest(
                employee_id=alice.id,
                leave_type=LeaveTypeEnum.annual,
                start_date=date(2026, 6, 10),
                end_date=date(2026, 6, 14),
                days=5,
                reason="Family vacation",
                status=LeaveStatusEnum.pending,
            ),
            LeaveRequest(
                employee_id=bob.id,
                leave_type=LeaveTypeEnum.sick,
                start_date=date(2026, 5, 20),
                end_date=date(2026, 5, 22),
                days=3,
                reason="Medical treatment",
                status=LeaveStatusEnum.approved,
                approved_by=sarah.id,
            ),
            LeaveRequest(
                employee_id=grace.id,
                leave_type=LeaveTypeEnum.annual,
                start_date=date(2026, 7, 1),
                end_date=date(2026, 7, 5),
                days=5,
                reason="Personal travel",
                status=LeaveStatusEnum.pending,
            ),
        ]
        for leave in leaves:
            db.add(leave)
        db.commit()
        print(f"   ✅ {len(leaves)} leave requests created")

        # ── Performance Reviews ───────────────────────────────────────
        reviews = [
            PerformanceReview(
                employee_id=alice.id,
                reviewer_id=sarah.id,
                period="2025-Q4",
                score=4.5,
                comments="Excellent performance. Delivered all projects on time."
            ),
            PerformanceReview(
                employee_id=bob.id,
                reviewer_id=sarah.id,
                period="2025-Q4",
                score=4.0,
                comments="Good analytical work. Needs improvement in communication."
            ),
            PerformanceReview(
                employee_id=grace.id,
                reviewer_id=sarah.id,
                period="2025-Q4",
                score=3.8,
                comments="Creative campaigns. Meeting targets consistently."
            ),
        ]
        for review in reviews:
            db.add(review)
        db.commit()
        print(f"   ✅ {len(reviews)} performance reviews created")

        print("\n🎉 Database seeded successfully!")
        print("\n📋 Login credentials:")
        print("   Admin:    admin@limkokwing.edu.sl  / Admin1234")
        print("   Manager:  sarah@limkokwing.edu.sl  / Manager1234")
        print("   Employee: alice@limkokwing.edu.sl  / Employee1234")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed()