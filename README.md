🚀I‑Campus – Next‑Gen Smart Campus Management System
I‑Campus is a multi‑tenant, AI‑ready, IoT‑enabled campus OS that automates the complete student lifecycle from admission to placement, with deep support for multi‑branch institutions, strict role‑based access control, and minimal manual intervention.

Backed by FastAPI + SQL Server and designed for web, mobile, and desktop frontends, I‑Campus aims to be a modern, extensible platform that can stay relevant for the next 10–20 years.

✨ Key Highlights
End‑to‑end automation: Admissions, academics, attendance, exams, fees, hostel, transport, canteen, library, placement, alumni, audit, and more.

Multi‑tenant & multi‑branch:

Tenants = institutions.

Campuses = branches per institution.

All data is scoped by tenant + campus.

24+ role‑based dashboards:

Super Admin, MD, Principal, Vice Principal, Admin, HOD, Class Coordinator, Faculty, Student, Parent, HR, Accounts, Hostel, Canteen, Transport, Library, Placement, Security, Stores, Maintenance, Audit, R&D, etc.

Access hardware integration:

RFID at gates, hostel, canteen, buses, library.

Biometric at classrooms and secure zones.

Mobile QR as optional low‑cost alternative.

AI & analytics ready:

Per‑role dashboards with KPIs, trend charts, alerts.

Planned AI assistant for queries like “show my attendance” or “next exam date”.

🏛 Current Backend Stack
Language: Python 3.13

Framework: FastAPI

Database: SQL Server (via SQLAlchemy + pyodbc)

Auth: JWT (OAuth2 Password flow with python‑jose)

ORM: SQLAlchemy

Migrations: (to be added later – Alembic planned)

Implemented so far
Project structured as a real backend service (app/ package):

core/ – configuration (SQL Server, JWT), security (hashing, JWT helpers)

db/ – models (Tenant, Campus, Role, User), session, init

schemas/ – Pydantic models for auth, users, tenants

api/v1/ – versioned routers (auth, tenants, campuses, users)

api/deps.py – shared dependencies (get_current_user, require_role)

Multi‑tenancy base:

Tenant model for institutions.

Campus model linked to tenant.

User linked to tenant + campus + role.

Role model for system roles (SUPER_ADMIN, etc.).

Security & auth:

Password hashing using passlib[bcrypt].

JWT token generation with configurable expiry.

/api/v1/auth/login issues access tokens.

get_current_user + require_role([...]) for protecting routes.

Working APIs:

Auth

POST /api/v1/auth/login – login with username/password, get JWT.

Tenants

GET /api/v1/tenants/ – list active tenants.

POST /api/v1/tenants/ – create tenant (SUPER_ADMIN only).

GET /api/v1/tenants/{id} – get one tenant.

DELETE /api/v1/tenants/{id} – soft delete (SUPER_ADMIN only).

Campuses

GET /api/v1/campuses/ – list campuses.

POST /api/v1/campuses/ – create campus for a tenant (SUPER_ADMIN only).

Users

Basic create/list endpoints wired to services (being upgraded with role checks).

Health

/health – simple health check.

/db-check – DB connectivity test (SELECT 1).

🧩 Planned Major Features (Roadmap Snapshot)
The functional map is large; this is a high‑level view.

Admission Management

Enquiry → application → document upload → entrance test → token → provisional seat → final confirmation.

Auto‑generated Student IDs (BRANCH+COURSE+BATCH+SERIAL), emails, default passwords (DOB).

Advanced Exam System

Mid/Final/Internal exam schema, customizable per institution.

Part A (online MCQ), Part B (offline descriptive) structure.

Question banks, hall tickets, grading, revaluation workflows.

Blockchain‑backed certificates/marks cards (planned).

Smart Attendance

RFID at gate (campus in/out).

Biometric at classroom for lecture attendance.

Grace period + latecomer ladder:

3 lates = warnings, 5th = suspension, notifications to all related roles.

“In campus / off campus” tracking; detection of bunking/unauthorized exit.

Canteen, Hostel, Library, Transport

RFID/bio‑based access and billing.

Automatic monthly mess/transport charges added to fee ledger.

Receipts and statements accessible to students and parents.

Dashboards & Analytics

Per‑role dashboards (24 modules) with:

KPI cards, charts, alerts, AI insights.

MIS reports and embedded audit logs.

Company Admin / SaaS Onboarding

One‑time tenant registration link.

Company verification workflow.

Auto‑provision tenant + Super Admin after approval.

Platform‑wide monitoring, logging, and support tools.

🚀 Getting Started (Backend Only)
1. Clone the repository
bash
git clone https://github.com/<your-username>/I-Campus.git
cd I-Campus/backend
2. Create and activate virtualenv
bash
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate   # Linux/macOS
3. Install dependencies
bash
pip install -r requirements.txt
If requirements.txt is not yet generated:

bash
pip install fastapi uvicorn sqlalchemy pyodbc python-jose[cryptography] passlib[bcrypt] python-multipart pydantic-settings
pip freeze > requirements.txt
4. Configure database & JWT
Check app/core/config.py and adjust for your environment:

SQL Server connection (SQLSERVER_SERVER, SQLSERVER_USER, SQLSERVER_PASSWORD, SQLSERVER_DB, SQLSERVER_DRIVER).

JWT settings (JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES).

Optionally, create a .env file to override defaults.

5. Run the server
From backend folder:

bash
uvicorn --app-dir . app.main:app --reload
Open:

Swagger UI: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

DB check: http://127.0.0.1:8000/db-check

6. Initial testing (JWT flow)
Seed DB with:

One Role row: SUPER_ADMIN.

One Tenant.

One Campus for that tenant.

One User with:

role_id → SUPER_ADMIN’s id

tenant_id, campus_id

hashed_password using the project’s get_password_hash().

In Swagger:

POST /api/v1/auth/login → use super admin username/password.

Copy access_token.

Click Authorize → use Bearer <token>.

Call:

GET /api/v1/tenants/

POST /api/v1/tenants/

GET /api/v1/campuses/

POST /api/v1/campuses/

🧱 Project Structure (Backend)
text
backend/
  app/
    main.py
    __init__.py

    api/
      deps.py
      __init__.py
      v1/
        auth.py
        tenants.py
        campuses.py
        users.py
        __init__.py

    core/
      config.py
      security.py
      __init__.py

    db/
      base.py
      init_db.py
      models.py
      session.py
      __init__.py

    schemas/
      auth.py
      user.py
      tenant.py
      __init__.py

    services/
      user_service.py
      tenant_service.py
      __init__.py
This layout keeps the API versioned, separates concerns (core, db, schemas, services), and is ready to grow into multiple micro‑modules.

💼 Why this project is interesting (for interviewers / reviewers)
Demonstrates realistic multi‑tenant SaaS design (tenants, campuses, roles, scoped data).

Shows production‑style FastAPI backend with:

Layered architecture (API, services, schemas, models).

JWT authentication and role‑based authorization.

SQL Server used from Python with SQLAlchemy (not just SQLite/Postgres demos).

Encodes complex domain logic:

Educational workflows (admission, exams, attendance).

Hardware integration (RFID, biometric, QR).

Discipline and policy automation (latecomers, leave, approvals).

Designed with a long‑term product vision, not just a CRUD sample:

24 role modules, ~180 submodules.

Future AI, IoT, blockchain integrations and analytics.

📌 Next Steps (Planned)
Complete role‑aware Users API (company admin, super admin, campus admin, etc.).

Add core attendance + timetable + calendar models and endpoints.

Start React frontend:

Login page → JWT handling.

Super Admin dashboard with tenants/campuses/users management.

Add logging, metrics, and audit trail middleware.

Deploy to cloud (Azure/AWS) and set up CI/CD.

👤 About the Author
Replace this section with your real details.

Name: Thilak A R

Role: Aspiring Devops & Software Architect

Focus: Python, FastAPI, SQL Server, full‑stack systems for education and automation.

LinkedIn: https://www.linkedin.com/in/thilak-a-r/

GitHub: https://github.com/Thilak-AR
