"""
Seed script — run once to populate the database with sample data.
Usage: python seed.py
Authors: Ramadan, Alhaji Kesuma Kamara, Dwight Doherty
Course: PROG315 - Object Oriented Programming 2
University: Limkokwing University of Creative Technology, Sierra Leone
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
        if db.query(Employee).count() > 0:
            print("Database already has data. Clear it first.")
            return

        print("Seeding database...")

        # ── Departments ───────────────────────────────────────────────
        departments = [
            Department(name="Human Resources",    description="Manages employee welfare and recruitment in Sierra Leone"),
            Department(name="Engineering",         description="Software development and IT infrastructure"),
            Department(name="Finance",             description="Financial planning and payroll management"),
            Department(name="Marketing",           description="Brand management and community outreach"),
            Department(name="Operations",          description="Day-to-day business operations"),
        ]
        for dept in departments:
            db.add(dept)
        db.commit()
        print(f"   {len(departments)} departments created")

        hr_dept  = db.query(Department).filter(Department.name == "Human Resources").first()
        eng_dept = db.query(Department).filter(Department.name == "Engineering").first()
        fin_dept = db.query(Department).filter(Department.name == "Finance").first()
        mkt_dept = db.query(Department).filter(Department.name == "Marketing").first()
        ops_dept = db.query(Department).filter(Department.name == "Operations").first()

        # ── Employees ─────────────────────────────────────────────────
        employees_data = [
            Employee(
                full_name="Arthakusie Ramadan Bangura",
                email="ramadan@limkokwing.edu.sl",
                hashed_password=hash_password("Admin1234"),
                phone="+232-76-100001",
                job_title="System Administrator",
                hire_date=date(2022, 1, 10),
                role=RoleEnum.admin,
                status=StatusEnum.active,
                department_id=hr_dept.id
            ),
            Employee(
                full_name="Alhaji Kesuma Kamara",
                email="kesuma@limkokwing.edu.sl",
                hashed_password=hash_password("Manager1234"),
                phone="+232-76-100002",
                job_title="HR Manager",
                hire_date=date(2022, 3, 15),
                role=RoleEnum.manager,
                status=StatusEnum.active,
                department_id=hr_dept.id
            ),
            Employee(
                full_name="Dwight Doherty",
                email="dwight@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-100003",
                job_title="Software Engineer",
                hire_date=date(2023, 1, 20),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=eng_dept.id
            ),
            Employee(
                full_name="Aminata Sesay",
                email="aminata@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-100004",
                job_title="Financial Analyst",
                hire_date=date(2023, 4, 10),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=fin_dept.id
            ),
            Employee(
                full_name="Mohamed Bangura",
                email="mohamed@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-100005",
                job_title="Marketing Specialist",
                hire_date=date(2023, 6, 1),
                role=RoleEnum.employee,
                status=StatusEnum.active,
                department_id=mkt_dept.id
            ),
            Employee(
                full_name="Fatmata Koroma",
                email="fatmata@limkokwing.edu.sl",
                hashed_password=hash_password("Employee1234"),
                phone="+232-76-100006",
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
        print(f"   {len(employees_data)} employees created")

        ramadan = db.query(Employee).filter(Employee.email == "ramadan@limkokwing.edu.sl").first()
        kesuma  = db.query(Employee).filter(Employee.email == "kesuma@limkokwing.edu.sl").first()
        dwight  = db.query(Employee).filter(Employee.email == "dwight@limkokwing.edu.sl").first()
        aminata = db.query(Employee).filter(Employee.email == "aminata@limkokwing.edu.sl").first()
        mohamed = db.query(Employee).filter(Employee.email == "mohamed@limkokwing.edu.sl").first()
        fatmata = db.query(Employee).filter(Employee.email == "fatmata@limkokwing.edu.sl").first()

        # ── Salaries ──────────────────────────────────────────────────
        salaries = [
            Salary(employee_id=ramadan.id, amount=120000, currency="SLL", effective_date=date(2022, 1, 10)),
            Salary(employee_id=kesuma.id,  amount=95000,  currency="SLL", effective_date=date(2022, 3, 15)),
            Salary(employee_id=dwight.id,  amount=85000,  currency="SLL", effective_date=date(2023, 1, 20)),
            Salary(employee_id=aminata.id, amount=80000,  currency="SLL", effective_date=date(2023, 4, 10)),
            Salary(employee_id=mohamed.id, amount=75000,  currency="SLL", effective_date=date(2023, 6,  1)),
            Salary(employee_id=fatmata.id, amount=70000,  currency="SLL", effective_date=date(2024, 1,  5)),
        ]
        for salary in salaries:
            db.add(salary)
        db.commit()
        print(f"   {len(salaries)} salary records created")

        # ── Attendance ────────────────────────────────────────────────
        attendances = [
            Attendance(
                employee_id=dwight.id,
                date=date.today(),
                clock_in=datetime.now(timezone.utc),
                status="open"
            ),
            Attendance(
                employee_id=aminata.id,
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
        print(f"   {len(attendances)} attendance records created")

        # ── Leave Requests ────────────────────────────────────────────
        leaves = [
            LeaveRequest(
                employee_id=dwight.id,
                leave_type=LeaveTypeEnum.annual,
                start_date=date(2026, 6, 10),
                end_date=date(2026, 6, 14),
                days=5,
                reason="Family event in Kenema",
                status=LeaveStatusEnum.pending,
            ),
            LeaveRequest(
                employee_id=aminata.id,
                leave_type=LeaveTypeEnum.sick,
                start_date=date(2026, 5, 20),
                end_date=date(2026, 5, 22),
                days=3,
                reason="Medical treatment at Connaught Hospital",
                status=LeaveStatusEnum.approved,
                approved_by=kesuma.id,
            ),
            LeaveRequest(
                employee_id=mohamed.id,
                leave_type=LeaveTypeEnum.annual,
                start_date=date(2026, 7, 1),
                end_date=date(2026, 7, 5),
                days=5,
                reason="Personal travel to Bo",
                status=LeaveStatusEnum.pending,
            ),
        ]
        for leave in leaves:
            db.add(leave)
        db.commit()
        print(f"   {len(leaves)} leave requests created")

        # ── Performance Reviews ───────────────────────────────────────
        reviews = [
            PerformanceReview(
                employee_id=dwight.id,
                reviewer_id=kesuma.id,
                period="2025-Q4",
                score=4.5,
                comments="Excellent software development skills. Delivered all tasks on time."
            ),
            PerformanceReview(
                employee_id=aminata.id,
                reviewer_id=kesuma.id,
                period="2025-Q4",
                score=4.0,
                comments="Strong financial analysis. Good attention to detail."
            ),
            PerformanceReview(
                employee_id=mohamed.id,
                reviewer_id=kesuma.id,
                period="2025-Q4",
                score=3.8,
                comments="Creative marketing campaigns. Consistently meeting targets."
            ),
        ]
        for review in reviews:
            db.add(review)
        db.commit()
        print(f"   {len(reviews)} performance reviews created")

        print("\nDatabase seeded successfully!")
        print("\nLogin credentials:")
        print("   Admin:    ramadan@limkokwing.edu.sl  / Admin1234")
        print("   Manager:  kesuma@limkokwing.edu.sl   / Manager1234")
        print("   Employee: dwight@limkokwing.edu.sl   / Employee1234")

    except Exception as e:
        db.rollback()
        print(f"Seeding failed: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    seed()