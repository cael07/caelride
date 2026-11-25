import os
import sys

# Ensure backend can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

from backend.database import SessionLocal, engine, DATABASE_URL, check_db_health, db_mode
from sqlalchemy import text

print(f"============================================================")
print(f"  CAEL RIDE — DATABASE HEALTH & STATUS CHECK")
print(f"============================================================")
print(f"Active Mode : {db_mode.upper()}")
print(f"Database URL: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else DATABASE_URL}")
print(f"Connection  : {'HEALTHY (Connected successfully!)' if check_db_health() else 'FAILED'}")
print(f"============================================================\n")

with SessionLocal() as session:
    print("=== Registered Users in Active Database ===")
    users = session.execute(text("SELECT id, username, email, role, is_active, is_activated, balance FROM auth_users LIMIT 10")).fetchall()
    if not users:
        print("  No users found.")
    for u in users:
        print(f"  ID={u[0]} | username={u[1]:15s} | email={u[2]:25s} | role={u[3]:12s} | active={u[4]} | activated={u[5]} | balance=PHP {u[6]:.2f}")

    print("\n=== Recent Ride Bookings ===")
    try:
        bookings = session.execute(text("SELECT id, passenger_id, driver_id, status, amount, created_at FROM ride_bookings ORDER BY id DESC LIMIT 5")).fetchall()
        if not bookings:
            print("  No bookings recorded yet.")
        for b in bookings:
            print(f"  Booking #{b[0]} | passenger={b[1]} | driver={b[2]} | status={b[3]} | amount={b[4]} | time={b[5]}")
    except Exception as e:
        print(f"  Bookings query error: {e}")

print("\n=== driver_docs/ Folder Contents ===")
driver_docs = os.path.join("backend", "driver_docs")
if os.path.exists(driver_docs):
    files = os.listdir(driver_docs)
    for f in files[:10]:
        size = os.path.getsize(os.path.join(driver_docs, f))
        print(f"  {f} ({size} bytes)")
else:
    print("  (folder not found)")

print("\n[OK] Done.")
