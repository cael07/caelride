from __future__ import annotations
import os
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Annotated, Optional, List

from ..database import get_db
from . import service
from .schemas import UserRegister, RegisterRequest, UserLogin, TokenPair, UserOut, RefreshRequest, MessageResponse, UpdateBalanceRequest, LoadBalanceGcashQrRequest, FixTopUpReferenceRequest, RolePermissionSave, CreateSupportTicket, SendSupportMessage, ClaimSupportTicket
from .models import SupportTicket, SupportMessage, User, Employee, BalanceLog
from .utils import create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

def is_admin_or_employee(user) -> bool:
    return bool(user and user.role not in ("passenger", "driver"))


@router.post("/register", response_model=TokenPair)
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db)
):
    try:
        user, access, refresh = service.register_user(
            db,
            request.user,
            request.face_image,
            request.app_id,
            license_image_b64=request.license_image,
            or_image_b64=request.or_image,
            cr_image_b64=request.cr_image,
        )
        return {
            "access_token": access,
            "refresh_token": refresh,
            "user": user
        }

    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        print(f"REGISTER ERROR:\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/login", response_model=TokenPair)
def login(
    credentials: UserLogin,
    app_id: str | None = None,
    db: Session = Depends(get_db)
):
    user, access, refresh = service.login_user(db, credentials, app_id)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "user": user
    }

from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)

@router.get("/me", response_model=UserOut)
def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user = service.get_current_user_from_token(db, token)
    return user

@router.post("/refresh")
def refresh_token(
    request: RefreshRequest,
    db: Session = Depends(get_db)
):
    from .utils import decode_token
    payload = decode_token(request.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    user_id = payload.get("sub")
    user = service.get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    new_access = create_access_token({"sub": str(user.id)})
    return {"access_token": new_access}

@router.get("/image/{username}")
def get_user_image(username: str, db: Session = Depends(get_db)):
    user = service.get_user_by_username(db, username)
    if not user or not user.face_image_path:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Path to the actual file
    from .service import FACE_IMAGES_DIR
    file_path = os.path.join(os.path.dirname(FACE_IMAGES_DIR), user.face_image_path)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
        
    from fastapi.responses import FileResponse
    return FileResponse(file_path, media_type="image/jpeg")

@router.get("/users")
def get_all_users(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Not authorized. Admin/Employee access only.")
    
    users = db.query(service.User).all()
    from .models import Employee
    employees = db.query(Employee).all()
    emp_map = {e.username.lower(): e for e in employees if e.username}

    # Serialize cleanly with employee details
    out = []
    for u in users:
        emp = emp_map.get(u.username.lower()) if u.username else None
        out.append({
            "id": u.id,
            "full_name": u.full_name,
            "username": u.username,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
            "is_activated": u.is_activated,
            "balance": u.balance or 0.0,
            "created_at": u.created_at.isoformat() if u.created_at else None,
            "department": emp.department if emp else None,
            "position": emp.position if emp else None,
            "location": emp.location if emp else None,
            "age": emp.age if emp else None,
            "sex": emp.sex if emp else None,
        })
    return out

@router.post("/users/{user_id}/toggle-active")
def toggle_user_active(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Not authorized. Admin/Employee access only.")
    
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_active = not user.is_active
    db.commit()
    return {"ok": True, "username": user.username, "is_active": user.is_active}

@router.post("/users/{user_id}/toggle-activated")
def toggle_user_activated(
    user_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Not authorized. Admin/Employee access only.")
    
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    user.is_activated = not user.is_activated
    db.commit()
    return {"ok": True, "username": user.username, "is_activated": user.is_activated}

@router.post("/users/{user_id}/update-balance")
async def update_balance(
    user_id: int,
    payload: UpdateBalanceRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Not authorized. Admin/Employee access only.")
    
    user = service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        
    if user.balance is None:
        user.balance = 0.0
    user.balance += payload.amount
    
    # Log the balance modification
    from .models import BalanceLog
    import random
    import json
    from datetime import datetime
    prefix = "F" if payload.amount < 0 else "S"
    now = datetime.utcnow()
    date_str = now.strftime("%y%m%d%H%M%S")
    rand5 = f"{random.randint(10000, 99999)}"
    sys_ref = f"CAEL-{prefix}{date_str}{rand5}"

    log_entry = BalanceLog(
        user_id=user.id,
        created_by_id=current_user.id,
        amount=payload.amount,
        new_balance=user.balance,
        reference_number=sys_ref,
        payment_method="system"
    )
    db.add(log_entry)
    db.commit()

    # Broadcast real-time top-up event to Admin sockets
    try:
        from ..ride.router import manager
        await manager.broadcast(json.dumps({
            "type": "top_up_created",
            "log": {
                "id": log_entry.id,
                "username": user.username,
                "full_name": user.full_name,
                "created_by": current_user.username,
                "amount": payload.amount,
                "new_balance": user.balance,
                "reference_number": sys_ref,
                "system_ref": sys_ref,
                "payment_method": "system",
                "created_at": now.isoformat(),
                "type": "fee" if payload.amount < 0 else "load"
            }
        }))
    except Exception as e:
        print("[WS Broadcast Error in update_balance]:", e)

    return {"ok": True, "username": user.username, "balance": user.balance}

@router.get("/balance-logs")
def get_balance_logs(
    page: int = Query(0),
    limit: int = Query(0),
    search: str = Query(""),
    status_filter: str = Query(""),
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    
    from .models import BalanceLog, User
    from sqlalchemy.orm import joinedload
    import sqlalchemy as sa
    
    query = db.query(BalanceLog)\
        .options(joinedload(BalanceLog.user), joinedload(BalanceLog.created_by))
        
    if not is_admin_or_employee(current_user):
        query = query.filter(BalanceLog.user_id == current_user.id)
        
    if search and search.strip():
        s = f"%{search.strip().lower()}%"
        query = query.join(BalanceLog.user).filter(
            sa.or_(
                sa.func.lower(User.username).like(s),
                sa.func.lower(User.full_name).like(s),
                sa.func.lower(BalanceLog.reference_number).like(s)
            )
        )
        
    if status_filter and status_filter.strip() and status_filter.strip().lower() != "all":
        raw_st = status_filter.strip().lower()
        if raw_st in ("approved", "verified"):
            query = query.filter(sa.or_(BalanceLog.status == "approved", BalanceLog.status == "verified", BalanceLog.status == None))
        elif raw_st in ("rejected", "unverified"):
            query = query.filter(sa.or_(BalanceLog.status == "rejected", BalanceLog.status == "unverified"))
        elif raw_st == "pending":
            query = query.filter(BalanceLog.status == "pending")
        else:
            query = query.filter(BalanceLog.status == raw_st)
        
    if page > 0 and limit > 0:
        raw_logs = query.order_by(BalanceLog.created_at.desc()).offset((page - 1) * limit).limit(limit + 1).all()
        has_more = len(raw_logs) > limit
        logs = raw_logs[:limit]
        is_paginated = True
    else:
        logs = query.order_by(BalanceLog.created_at.desc()).limit(100).all()
        has_more = False
        is_paginated = False
    
    out = []
    for lg in logs:
        is_fee = False
        if (lg.amount or 0) < 0 or (lg.reference_number and lg.reference_number.endswith("-F")):
            is_fee = True
        elif not lg.reference_number:
            creator = lg.created_by
            if creator and creator.role == "driver":
                is_fee = True
                
        ref_str = (lg.reference_number or "").lower()
        method = (lg.payment_method or ("maya" if "maya" in ref_str else ("gcash" if lg.reference_number else "system"))).lower()
        prefix = "M" if "maya" in method else ("G" if "gcash" in method else "F")
        
        dt = lg.created_at or datetime.utcnow()
        date_str = dt.strftime("%y%m%d%H%M%S")
        rand5 = f"{(lg.id * 12345 + 54321) % 90000 + 10000}"
        sys_ref = f"CAEL-{prefix}{date_str}{rand5}"
        
        out.append({
            "id": lg.id,
            "username": lg.user.username if lg.user else "Unknown",
            "full_name": lg.user.full_name if lg.user else "Unknown",
            "created_by": lg.created_by.username if lg.created_by else "Unknown",
            "amount": lg.amount,
            "new_balance": lg.new_balance,
            "reference_number": lg.reference_number,
            "system_ref": sys_ref,
            "payment_method": method,
            "status": lg.status or "approved",
            "created_at": lg.created_at.isoformat() if lg.created_at else None,
            "type": "fee" if is_fee else "load"
        })

    if is_paginated:
        return {
            "items": out,
            "page": page,
            "limit": limit,
            "has_more": has_more
        }
    return out

@router.get("/balance-stats")
def get_balance_stats(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Not authorized. Admin/Employee access only.")
    
    from .models import BalanceLog
    from sqlalchemy.orm import joinedload
    logs = db.query(BalanceLog).options(joinedload(BalanceLog.created_by)).order_by(BalanceLog.created_at.asc()).all()
    
    daily_load_changes = {}
    daily_fee_changes = {}
    all_dates = set()
    
    for lg in logs:
        if lg.created_at:
            date_str = lg.created_at.strftime("%Y-%m-%d")
            all_dates.add(date_str)
            
            is_fee = False
            if (lg.amount or 0) < 0 or (lg.reference_number and lg.reference_number.endswith("-F")):
                is_fee = True
            elif not lg.reference_number:
                creator = lg.created_by
                if creator and creator.role == "driver":
                    is_fee = True
                    
            if is_fee:
                daily_fee_changes[date_str] = daily_fee_changes.get(date_str, 0.0) + abs(lg.amount or 0.0)
            else:
                daily_load_changes[date_str] = daily_load_changes.get(date_str, 0.0) + (lg.amount or 0.0)
                
    running_load = 0.0
    running_fee = 0.0
    out = []
    
    for date_str in sorted(all_dates):
        load_change = daily_load_changes.get(date_str, 0.0)
        fee_change = daily_fee_changes.get(date_str, 0.0)
        
        running_load += load_change
        running_fee += fee_change
        
        out.append({
            "date": date_str,
            "load_change": load_change,
            "load_total": running_load,
            "fee_change": fee_change,
            "fee_total": running_fee
        })
        
    if not out:
        from datetime import datetime
        import sqlalchemy as sa
        total_sys = db.query(sa.func.sum(service.User.balance)).scalar() or 0.0
        out.append({
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "load_change": 0.0,
            "load_total": total_sys,
            "fee_change": 0.0,
            "fee_total": 0.0
        })
        
    return out

@router.get("/bookings")
def get_admin_bookings(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    
    from .models import Booking
    
    query = db.query(Booking)
    if is_admin_or_employee(current_user):
        query = query.filter(Booking.status.in_(["accepted", "completed", "cancelled"]))
    elif current_user.role == "driver":
        query = query.filter(Booking.driver_id == current_user.id, Booking.status.in_(["completed", "cancelled"]))
    else: # passenger
        query = query.filter(Booking.passenger_id == current_user.id, Booking.status.in_(["completed", "cancelled"]))
        
    bookings = query.order_by(Booking.created_at.desc()).all()
    
    out = []
    for b in bookings:
        passenger = service.get_user_by_id(db, b.passenger_id)
        driver = service.get_user_by_id(db, b.driver_id) if b.driver_id else None
        
        out.append({
            "id": b.id,
            "passenger": passenger.full_name if passenger else "Passenger",
            "passenger_username": passenger.username if passenger else "Passenger",
            "driver": driver.full_name if driver else "Unassigned",
            "driver_username": driver.username if driver else "Unassigned",
            "pickup": b.pickup_address if b.pickup_address else f"{b.pickup_lat:.4f}, {b.pickup_lng:.4f}",
            "dropoff": b.dropoff_address if b.dropoff_address else f"{b.dropoff_lat:.4f}, {b.dropoff_lng:.4f}",
            "amount": b.amount or 0.0,
            "status": b.status,
            "date": b.created_at.isoformat() if b.created_at else None,
            "document_image": b.document_image,
            "document_info": b.document_info,
            "document_tip": b.document_tip,
            "received_image": b.received_image,
            "signature_image": b.signature_image
        })
    return out

@router.get("/health")
def health():
    import os
    from ..database import check_db_health
    db_ok = check_db_health()
    return {
        "status": "ok",
        "database": "online" if db_ok else "offline",
        "service": "pythonlogin-auth"
    }


@router.post("/load-balance-gcash-qr")
async def load_balance_gcash_qr(
    payload: LoadBalanceGcashQrRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if current_user.role != "driver":
        raise HTTPException(status_code=403, detail="Only drivers can load balance via GCash")
    
    if payload.amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")
        
    ref_num = (payload.reference_number or "").strip().replace(" ", "")
    if not ref_num or len(ref_num) < 3:
        raise HTTPException(status_code=400, detail="Please enter a valid reference number.")
        
    # Check for double submission / reuse of reference number
    from .models import BalanceLog
    existing_log = db.query(BalanceLog).filter(BalanceLog.reference_number == ref_num).first()
    if existing_log:
        raise HTTPException(status_code=400, detail="This GCash reference number has already been claimed.")
        
    # Do NOT auto-credit driver balance. Set status to pending for Admin verification.
    import random
    import json
    from datetime import datetime
    method_str = (getattr(payload, "payment_method", None) or "gcash").lower()
    log_entry = BalanceLog(
        user_id=current_user.id,
        created_by_id=current_user.id,  # Self top-up
        amount=payload.amount,
        new_balance=current_user.balance or 0.0,
        reference_number=ref_num,
        payment_method=method_str,
        status="pending"
    )
    db.add(log_entry)
    db.commit()
    db.refresh(log_entry)
    
    # Generate system reference format: CAEL-GyyMMDDhis + 5 random digits (for GCash) / CAEL-MyyMMDDhis + 5 random digits (for Maya)
    method = (getattr(payload, "payment_method", None) or "gcash").lower()
    prefix = "M" if "maya" in method else "G"
    now = datetime.utcnow()
    date_str = now.strftime("%y%m%d%H%M%S")
    rand5 = f"{random.randint(10000, 99999)}"
    system_ref = f"CAEL-{prefix}{date_str}{rand5}"

    # Broadcast real-time top-up event to Admin WebSockets
    try:
        from ..ride.router import manager
        await manager.broadcast(json.dumps({
            "type": "top_up_created",
            "log": {
                "id": log_entry.id,
                "username": current_user.username,
                "full_name": current_user.full_name,
                "created_by": current_user.username,
                "amount": payload.amount,
                "new_balance": current_user.balance or 0.0,
                "reference_number": ref_num,
                "system_ref": system_ref,
                "payment_method": method_str,
                "status": "pending",
                "created_at": now.isoformat(),
                "type": "load"
            }
        }))
    except Exception as e:
        print("[WS Broadcast Error in load_balance_gcash_qr]:", e)
    
    return {
        "ok": True,
        "message": f"Top up of ₱{payload.amount:.2f} submitted! Waiting for Admin approval.",
        "new_balance": current_user.balance or 0.0,
        "reference_number": ref_num,
        "system_ref": system_ref,
        "transaction_id": system_ref,
        "status": "pending",
        "log_id": log_entry.id
    }


@router.post("/topup/{log_id}/verify")
async def verify_topup(
    log_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Admin authorization required.")
        
    from .models import BalanceLog, User
    log_entry = db.query(BalanceLog).filter(BalanceLog.id == log_id).first()
    if not log_entry:
        raise HTTPException(status_code=404, detail="Top up record not found.")
        
    if log_entry.status == "approved":
        return {"ok": True, "message": "Top up is already approved.", "status": "approved"}
        
    driver = db.query(User).filter(User.id == log_entry.user_id).first()
    if driver:
        if driver.balance is None:
            driver.balance = 0.0
        driver.balance += log_entry.amount
        log_entry.new_balance = driver.balance
        
    log_entry.status = "approved"
    db.commit()
    db.refresh(log_entry)
    
    try:
        from ..ride.router import manager
        import json
        await manager.broadcast(json.dumps({
            "type": "top_up_status_updated",
            "log_id": log_id,
            "user_id": log_entry.user_id,
            "new_balance": driver.balance if driver else log_entry.new_balance,
            "status": "approved"
        }))
    except Exception as e:
        print("[WS Broadcast Error in verify_topup]:", e)
        
    return {"ok": True, "message": "Top up verified and credited successfully.", "status": "approved"}


@router.post("/topup/{log_id}/unverify")
async def unverify_topup(
    log_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Admin authorization required.")
        
    from .models import BalanceLog
    log_entry = db.query(BalanceLog).filter(BalanceLog.id == log_id).first()
    if not log_entry:
        raise HTTPException(status_code=404, detail="Top up record not found.")
        
    log_entry.status = "rejected"
    db.commit()
    db.refresh(log_entry)
    
    try:
        from ..ride.router import manager
        import json
        await manager.broadcast(json.dumps({
            "type": "top_up_status_updated",
            "log_id": log_id,
            "user_id": log_entry.user_id,
            "status": "rejected"
        }))
    except Exception as e:
        print("[WS Broadcast Error in unverify_topup]:", e)
        
    return {"ok": True, "message": "Top up marked as unverified.", "status": "rejected"}


@router.post("/topup/fix-reference")
async def fix_topup_reference(
    payload: FixTopUpReferenceRequest,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    
    sys_ref_input = (payload.system_ref or "").strip().upper()
    new_ref_input = (payload.new_reference_number or "").strip()
    
    if not sys_ref_input:
        raise HTTPException(status_code=400, detail="System Reference No. is required.")
    if not new_ref_input:
        raise HTTPException(status_code=400, detail="Top Up Reference No. is required.")
        
    from .models import BalanceLog
    logs = db.query(BalanceLog).filter(BalanceLog.user_id == current_user.id).all()
    target_log = None
    
    for lg in logs:
        dt = lg.created_at or datetime.utcnow()
        date_str = dt.strftime("%y%m%d%H%M%S")
        rand5 = f"{(lg.id * 12345 + 54321) % 90000 + 10000}"
        method = (lg.payment_method or "gcash").lower()
        prefix = "M" if "maya" in method else ("G" if "gcash" in method else "F")
        computed_sys_ref = f"CAEL-{prefix}{date_str}{rand5}"
        
        if (lg.reference_number and lg.reference_number.upper() == sys_ref_input) or computed_sys_ref.upper() == sys_ref_input:
            target_log = lg
            break
            
    if not target_log:
        raise HTTPException(status_code=400, detail="System Reference No. does not exist. Please check.")
        
    target_log.reference_number = new_ref_input
    target_log.status = "pending"
    db.commit()
    db.refresh(target_log)
    
    try:
        from ..ride.router import manager
        import json
        await manager.broadcast(json.dumps({
            "type": "top_up_created",
            "log": {
                "id": target_log.id,
                "username": current_user.username,
                "full_name": current_user.full_name,
                "created_by": current_user.username,
                "amount": target_log.amount,
                "new_balance": target_log.new_balance,
                "reference_number": new_ref_input,
                "system_ref": sys_ref_input,
                "payment_method": target_log.payment_method or "gcash",
                "created_at": target_log.created_at.isoformat() if target_log.created_at else datetime.utcnow().isoformat(),
                "status": "pending",
                "type": "load"
            }
        }))
    except Exception as e:
        print("[WS Broadcast Error in fix_topup_reference]:", e)
        
    return {"ok": True, "message": "Successfully Updated", "status": "pending"}


from .schemas import EmployeeCreate, EmployeeOut
from .models import Employee, User
from .utils import hash_password
from typing import List

@router.post("/employees", response_model=EmployeeOut)
def create_employee(
    payload: EmployeeCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
        
    # Check if username or email already exists
    existing_user = db.query(User).filter((User.username == payload.username) | (User.email == payload.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email is already registered")

    # Set employee User.role to their position (e.g. 'it_admin', 'hr_staff', 'staff_admin')
    pos_role = payload.position.strip().lower().replace(" ", "_")
    new_user = User(
        full_name=f"{payload.first_name} {payload.last_name}",
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        role=pos_role,  # Position set as role
        is_active=True,
        is_activated=True,
    )
    db.add(new_user)
    db.flush()

    employee = Employee(
        username=payload.username,
        first_name=payload.first_name,
        middle_name=payload.middle_name,
        last_name=payload.last_name,
        age=payload.age,
        sex=payload.sex,
        email=payload.email,
        address=payload.address,
        department=payload.department,
        position=payload.position,
        location=payload.location,
    )
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


@router.get("/employees", response_model=List[EmployeeOut])
def get_employees(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
        
    employees = db.query(Employee).order_by(Employee.created_at.desc()).all()
    return employees


@router.get("/role-permissions")
def get_role_permissions(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    return service.get_all_role_permissions(db)


@router.post("/role-permissions")
def save_role_permission_endpoint(
    payload: RolePermissionSave,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    current_user = service.get_current_user_from_token(db, token)
    if not is_admin_or_employee(current_user):
        raise HTTPException(status_code=403, detail="Permission denied")
    
    rec = service.save_role_permission(db, payload.role, payload.menu_access)
    return {
        "status": "success",
        "role": rec.role,
        "menu_access": payload.menu_access,
        "message": f"Permissions updated successfully for role '{payload.role}'"
    }


# ==========================================
# CHAT SUPPORT ENDPOINTS
# ==========================================

@router.post("/support/tickets")
def create_support_ticket(
    payload: CreateSupportTicket,
    db: Session = Depends(get_db)
):
    ticket = SupportTicket(
        user_id=payload.user_id,
        user_name=payload.user_name,
        user_role=payload.user_role or "Passenger",
        topic=payload.topic or "General Support",
        message_snippet=payload.message[:100],
        status="waiting"
    )
    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    msg = SupportMessage(
        ticket_id=ticket.id,
        sender_type="user",
        sender_name=payload.user_name,
        text=payload.message
    )
    db.add(msg)
    db.commit()

    return {
        "status": "success",
        "ticket_id": ticket.id,
        "message": "Support request submitted successfully. You are in the queue."
    }

@router.get("/support/tickets/my-active")
def get_my_active_support_ticket(
    user_name: str = Query(...),
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(
        SupportTicket.user_name == user_name,
        SupportTicket.status.in_(["waiting", "active"])
    ).order_by(SupportTicket.created_at.desc()).first()

    if not ticket:
        return {"ticket": None, "messages": []}

    messages = db.query(SupportMessage).filter(SupportMessage.ticket_id == ticket.id).order_by(SupportMessage.created_at.asc()).all()

    queue_position = 0
    if ticket.status == "waiting":
        queue_position = db.query(SupportTicket).filter(
            SupportTicket.status == "waiting",
            SupportTicket.id <= ticket.id
        ).count()

    return {
        "ticket": {
            "id": ticket.id,
            "user_name": ticket.user_name,
            "user_role": ticket.user_role,
            "topic": ticket.topic,
            "status": ticket.status,
            "agent_name": ticket.agent_name,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
            "queue_position": queue_position,
        },
        "messages": [
            {
                "id": m.id,
                "sender_type": m.sender_type,
                "sender_name": m.sender_name,
                "text": m.text,
                "created_at": m.created_at.strftime("%I:%M %p") if m.created_at else ""
            }
            for m in messages
        ]
    }

@router.get("/support/tickets/waiting")
def get_waiting_tickets(
    db: Session = Depends(get_db)
):
    tickets = db.query(SupportTicket).filter(SupportTicket.status == "waiting").order_by(SupportTicket.created_at.asc()).all()
    result = []
    for t in tickets:
        msg_count = db.query(SupportMessage).filter(SupportMessage.ticket_id == t.id).count()
        first_msg = db.query(SupportMessage).filter(SupportMessage.ticket_id == t.id).order_by(SupportMessage.created_at.asc()).first()
        result.append({
            "id": t.id,
            "user_name": t.user_name,
            "user_role": t.user_role,
            "topic": t.topic,
            "status": t.status,
            "message_snippet": t.message_snippet or (first_msg.text if first_msg else ""),
            "created_at": t.created_at.strftime("%I:%M %p") if t.created_at else "",
            "time_ago": "Just now",
            "message_count": msg_count
        })
    return result

@router.get("/support/tickets/active")
def get_active_tickets(
    agent_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(SupportTicket).filter(SupportTicket.status == "active")
    if agent_name:
        query = query.filter(SupportTicket.agent_name == agent_name)
    tickets = query.order_by(SupportTicket.updated_at.desc()).all()
    
    result = []
    for t in tickets:
        msg_count = db.query(SupportMessage).filter(SupportMessage.ticket_id == t.id).count()
        last_msg = db.query(SupportMessage).filter(SupportMessage.ticket_id == t.id).order_by(SupportMessage.created_at.desc()).first()
        result.append({
            "id": t.id,
            "user_name": t.user_name,
            "user_role": t.user_role,
            "topic": t.topic,
            "status": t.status,
            "agent_name": t.agent_name,
            "last_message": last_msg.text if last_msg else (t.message_snippet or ""),
            "last_time": last_msg.created_at.strftime("%I:%M %p") if (last_msg and last_msg.created_at) else "",
            "message_count": msg_count
        })
    return result

@router.get("/support/tickets/history")
def get_support_history(
    db: Session = Depends(get_db)
):
    tickets = db.query(SupportTicket).order_by(SupportTicket.created_at.desc()).limit(100).all()
    result = []
    for t in tickets:
        msg_count = db.query(SupportMessage).filter(SupportMessage.ticket_id == t.id).count()
        result.append({
            "id": t.id,
            "user_name": t.user_name,
            "user_role": t.user_role,
            "topic": t.topic,
            "status": t.status,
            "agent_name": t.agent_name or "Unassigned",
            "message_count": msg_count,
            "created_at": t.created_at.strftime("%Y-%m-%d %I:%M %p") if t.created_at else "",
            "resolved_at": t.resolved_at.strftime("%Y-%m-%d %I:%M %p") if t.resolved_at else (t.updated_at.strftime("%Y-%m-%d %I:%M %p") if t.updated_at else "")
        })
    return result

@router.post("/support/tickets/{ticket_id}/claim")
def claim_support_ticket(
    ticket_id: int,
    payload: ClaimSupportTicket,
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    from datetime import datetime
    ticket.status = "active"
    ticket.agent_name = payload.agent_name
    ticket.claimed_at = datetime.utcnow()
    db.commit()
    db.refresh(ticket)
    return {"status": "success", "ticket_id": ticket.id, "agent_name": ticket.agent_name}

@router.get("/support/tickets/{ticket_id}/messages")
def get_ticket_messages(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    messages = db.query(SupportMessage).filter(SupportMessage.ticket_id == ticket_id).order_by(SupportMessage.created_at.asc()).all()
    return {
        "ticket": {
            "id": ticket.id,
            "user_name": ticket.user_name,
            "user_role": ticket.user_role,
            "topic": ticket.topic,
            "status": ticket.status,
            "agent_name": ticket.agent_name,
            "created_at": ticket.created_at.isoformat() if ticket.created_at else None,
        },
        "messages": [
            {
                "id": m.id,
                "sender_type": m.sender_type,
                "sender_name": m.sender_name,
                "text": m.text,
                "created_at": m.created_at.strftime("%I:%M %p") if m.created_at else ""
            }
            for m in messages
        ]
    }

@router.post("/support/tickets/{ticket_id}/messages")
def send_ticket_message(
    ticket_id: int,
    payload: SendSupportMessage,
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    from datetime import datetime
    msg = SupportMessage(
        ticket_id=ticket.id,
        sender_type=payload.sender_type,
        sender_name=payload.sender_name,
        text=payload.text
    )
    db.add(msg)
    ticket.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(msg)
    return {
        "id": msg.id,
        "sender_type": msg.sender_type,
        "sender_name": msg.sender_name,
        "text": msg.text,
        "created_at": msg.created_at.strftime("%I:%M %p") if msg.created_at else ""
    }

@router.post("/support/tickets/{ticket_id}/resolve")
def resolve_support_ticket(
    ticket_id: int,
    db: Session = Depends(get_db)
):
    ticket = db.query(SupportTicket).filter(SupportTicket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    from datetime import datetime
    ticket.status = "resolved"
    ticket.resolved_at = datetime.utcnow()
    ticket.updated_at = datetime.utcnow()
    db.commit()
    return {"status": "success", "ticket_id": ticket.id}



