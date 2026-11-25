from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Load .env file from project root or backend directory if present
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(PROJECT_ROOT, ".env"))
    load_dotenv(os.path.join(BASE_DIR, ".env"))
except Exception:
    pass

# ============================================================================
# DUAL DATABASE SELECTION
# Path 1: Local SQLite database (backend/auth.db) - completely preserved!
# Path 2: Online Supabase PostgreSQL database (Tokyo ap-northeast-1)
# ============================================================================
DEFAULT_SQLITE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'auth.db')}"
DEFAULT_SUPABASE_URL = "postgresql://postgres.cchdtavgisogqcoixghz:N6CezCoRAcPXWhD0@aws-0-ap-northeast-1.pooler.supabase.com:5432/postgres"

# Determine active database mode: 'local' (sqlite) or 'supabase' (postgres)
db_mode = os.environ.get("DB_MODE", os.environ.get("DB_CHOICE", "supabase")).strip().lower()

if db_mode in ("sqlite", "local"):
    _url = os.environ.get("SQLITE_DATABASE_URL", DEFAULT_SQLITE_URL)
    print(f"DATABASE MODE: [PATH 1 - LOCAL SQLITE] -> {os.path.join(BASE_DIR, 'auth.db')}")
else:
    _url = os.environ.get("SUPABASE_DATABASE_URL", os.environ.get("DATABASE_URL", DEFAULT_SUPABASE_URL))
    # Automatically convert direct IPv6 hostname to high-speed IPv4 pooler if needed
    if "db.cchdtavgisogqcoixghz.supabase.co" in _url:
        _url = _url.replace("db.cchdtavgisogqcoixghz.supabase.co:5432", "aws-0-ap-northeast-1.pooler.supabase.com:5432")
        if "postgres.cchdtavgisogqcoixghz" not in _url:
            _url = _url.replace("postgres:", "postgres.cchdtavgisogqcoixghz:", 1)
    print("DATABASE MODE: [PATH 2 - ONLINE SUPABASE POSTGRESQL] -> Connected to project cchdtavgisogqcoixghz")

# Fix Render's legacy 'postgres://' for SQLAlchemy 2.0
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql://", 1)

DATABASE_URL = _url

# Configure engine with pooling suited for SQLite or PostgreSQL
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        from .auth.models import User, Booking, BalanceLog, Employee, RolePermission, SupportTicket, SupportMessage  # noqa: F401

        # Reset database for testing (drops only tables defined in this app)
        # print("DATABASE: Resetting auth_users table for testing...")
        # Base.metadata.drop_all(bind=engine)

        Base.metadata.create_all(bind=engine)

        with engine.connect() as conn:
            # All columns to auto-migrate (safe: silently ignored if column already exists)
            new_cols = [
                # Driver text metadata
                ("license_number",       "TEXT"),
                ("license_image_path",   "TEXT"),
                ("or_renewal_date",      "TEXT"),
                ("or_image_path",        "TEXT"),
                ("cr_plate_number",      "TEXT"),
                ("cr_brand",             "TEXT"),
                ("cr_color",             "TEXT"),
                ("cr_model",             "TEXT"),
                ("cr_owner_name",        "TEXT"),
                ("cr_image_path",        "TEXT"),
                # Base64 image columns stored in DB (persists on Render PostgreSQL)
                ("face_image_b64_db",    "TEXT"),
                ("license_image_b64_db", "TEXT"),
                ("or_image_b64_db",      "TEXT"),
                ("cr_image_b64_db",      "TEXT"),
                ("is_activated",         "BOOLEAN DEFAULT 0"),
                ("balance",              "FLOAT DEFAULT 0.0"),
            ]
            for col_name, col_type in new_cols:
                try:
                    conn.execute(text(f"ALTER TABLE auth_users ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    print(f"DATABASE: Added column {col_name} to auth_users.")
                except Exception:
                    pass  # Column already exists — safe to ignore

            # Auto-migrate amount column in ride_bookings table
            try:
                conn.execute(text("ALTER TABLE ride_bookings ADD COLUMN amount FLOAT DEFAULT 0.0"))
                conn.commit()
                print("DATABASE: Added column amount to ride_bookings.")
            except Exception:
                pass  # Column already exists

            # Auto-migrate pickup_address and dropoff_address columns in ride_bookings table
            for col_name in ["pickup_address", "dropoff_address"]:
                try:
                    conn.execute(text(f"ALTER TABLE ride_bookings ADD COLUMN {col_name} VARCHAR(500) NULL"))
                    conn.commit()
                    print(f"DATABASE: Added column {col_name} to ride_bookings.")
                except Exception:
                    pass  # Column already exists

            # Auto-migrate document_image, document_info, document_tip, received_image, signature_image columns in ride_bookings table
            for col_name, col_type in [("document_image", "TEXT"), ("document_info", "VARCHAR(1000)"), ("document_tip", "VARCHAR(1000)"), ("received_image", "TEXT"), ("signature_image", "TEXT")]:
                try:
                    conn.execute(text(f"ALTER TABLE ride_bookings ADD COLUMN {col_name} {col_type} NULL"))
                    conn.commit()
                    print(f"DATABASE: Added column {col_name} to ride_bookings.")
                except Exception:
                    pass  # Column already exists

            # Auto-migrate reference_number, payment_method, and status columns in auth_balance_logs table
            for col_name in ["reference_number", "payment_method", "status"]:
                try:
                    conn.execute(text(f"ALTER TABLE auth_balance_logs ADD COLUMN {col_name} TEXT DEFAULT 'approved'"))
                    conn.commit()
                    print(f"DATABASE: Added column {col_name} to auth_balance_logs.")
                except Exception:
                    pass  # Column already exists

            # Auto-migrate employees table columns
            for col_name, col_type in [
                ("username", "VARCHAR(80) NULL"),
                ("middle_name", "VARCHAR(100) NULL"),
                ("department", "VARCHAR(100) NULL"),
                ("position", "VARCHAR(100) NULL"),
                ("location", "VARCHAR(200) NULL")
            ]:
                try:
                    conn.execute(text(f"ALTER TABLE employees ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                    print(f"DATABASE: Added column {col_name} to employees.")
                except Exception:
                    pass  # Column already exists

        # Backfill reference_number for existing balance logs where reference_number is NULL
        from .auth.models import BalanceLog
        with SessionLocal() as session:
            try:
                null_logs = session.query(BalanceLog).filter(BalanceLog.reference_number == None).all()
                if null_logs:
                    for lg in null_logs:
                        is_fee = False
                        if lg.created_by and lg.created_by.role == "driver":
                            is_fee = True
                        dt = lg.created_at or datetime.utcnow()
                        date_str = dt.strftime("%y%m%d%H%M%S")
                        rand5 = f"{(lg.id * 12345 + 54321) % 90000 + 10000}"
                        prefix = "F" if is_fee else "S"
                        lg.reference_number = f"CAEL-{prefix}{date_str}{rand5}"
                        if not lg.payment_method:
                            lg.payment_method = "system"
                    session.commit()
                    print(f"DATABASE: Backfilled reference numbers for {len(null_logs)} balance log entries.")
            except Exception as e:
                print("Backfill error:", e)

            # Ensure GCash and Maya top up logs default to 'pending' if status is NULL or unverified
            try:
                gcash_maya_logs = session.query(BalanceLog).filter(
                    (BalanceLog.payment_method.in_(["gcash", "maya"])) & 
                    ((BalanceLog.status == None) | (BalanceLog.status == "approved"))
                ).all()
                if gcash_maya_logs:
                    for lg in gcash_maya_logs:
                        # If self top-up by driver via GCash or Maya, set to pending for Admin verification testing
                        if lg.user_id == lg.created_by_id or lg.payment_method in ["gcash", "maya"]:
                            lg.status = "pending"
                    session.commit()
                    print(f"DATABASE: Set {len(gcash_maya_logs)} GCash/Maya top-up entries to pending status.")
            except Exception as e:
                print("Status migration error:", e)

        print("DATABASE: Tables initialized successfully.")
        
        # Seed default super_admin user if none exists
        from .auth.models import User
        from .auth.utils import hash_password
        with SessionLocal() as session:
            super_admin_exists = session.query(User).filter(User.role == 'super_admin').first() is not None
            if not super_admin_exists:
                existing_email = session.query(User).filter(User.email == "caesarliteratus@gmail.com").first()
                existing_username = session.query(User).filter(User.username == "admin").first()
                if existing_email:
                    existing_email.role = "super_admin"
                    existing_email.is_active = True
                    existing_email.is_activated = True
                    if not existing_username:
                        existing_email.username = "admin"
                    session.commit()
                    print(f"DATABASE: Upgraded existing user with email {existing_email.email} to super_admin.")
                elif existing_username:
                    existing_username.role = "super_admin"
                    existing_username.is_active = True
                    existing_username.is_activated = True
                    session.commit()
                    print(f"DATABASE: Upgraded existing user with username {existing_username.username} to super_admin.")
                else:
                    print("DATABASE: Seeding default super_admin user...")
                    admin_user = User(
                        full_name="Super Administrator",
                        username="admin",
                        email="caesarliteratus@gmail.com",
                        password_hash=hash_password("12345678"),
                        role="super_admin",
                        is_active=True,
                        is_activated=True
                    )
                    session.add(admin_user)
                    session.commit()
                    print("DATABASE: Default super_admin user created successfully.")
                
    except Exception as e:
        print(f"DATABASE ERROR during init: {str(e)}")

def check_db_health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"DATABASE HEALTH CHECK FAILED: {str(e)}")
        return False
