from __future__ import annotations
import os
import base64
import uuid
import io
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from fastapi import HTTPException, status
from PIL import Image

import json
from .models import User, RolePermission
from .schemas import UserRegister, UserLogin
from .utils import hash_password, verify_password, create_access_token, create_refresh_token, decode_token

FACE_IMAGES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "face_images")
os.makedirs(FACE_IMAGES_DIR, exist_ok=True)

DRIVER_DOCS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "driver_docs")
os.makedirs(DRIVER_DOCS_DIR, exist_ok=True)


def normalize_base64(b64_data: str) -> str:
    """Ensure the base64 string has a data-URL prefix. Returns as-is if already prefixed."""
    if b64_data and not b64_data.startswith("data:"):
        return f"data:image/jpeg;base64,{b64_data}"
    return b64_data


def compress_image_base64(base64_data: str, quality: int = 75) -> str:
    """Compress a base64-encoded image using Pillow and return compressed base64 data-URL.
    Reduces storage size while keeping images usable for display."""
    try:
        raw = base64_data
        if "," in raw:
            raw = raw.split(",", 1)[1]
        img_bytes = base64.b64decode(raw)
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        output = io.BytesIO()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        compressed_b64 = base64.b64encode(output.getvalue()).decode("utf-8")
        return f"data:image/jpeg;base64,{compressed_b64}"
    except Exception as e:
        print(f"WARNING: Image compression failed: {e} — using original.")
        return normalize_base64(base64_data)


def get_user_by_id(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter(func.lower(User.username) == func.lower(username)).first()
    return user


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(func.lower(User.email) == func.lower(email)).first()


def register_user(
    db: Session,
    data: UserRegister,
    face_image_b64: str | None,
    app_id: str | None,
    license_image_b64: str | None = None,
    or_image_b64: str | None = None,
    cr_image_b64: str | None = None,
) -> tuple[User, str, str]:
    # Check uniqueness
    if get_user_by_username(db, data.username):
        raise HTTPException(status_code=400, detail="Username already taken")
    if get_user_by_email(db, data.email):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Compress images before storing in DB (reduce size while keeping quality)
    face_b64_compressed    = compress_image_base64(face_image_b64) if face_image_b64 else None
    license_b64_compressed = compress_image_base64(license_image_b64) if license_image_b64 else None
    or_b64_compressed      = compress_image_base64(or_image_b64) if or_image_b64 else None
    cr_b64_compressed      = compress_image_base64(cr_image_b64) if cr_image_b64 else None

    # If position is provided or role is an employee position, derive role from position
    if data.position:
        role_str = data.position.strip().lower().replace(" ", "_")
    elif data.role:
        role_str = data.role.strip().lower().replace(" ", "_") if data.role not in ("passenger", "driver", "admin", "super_admin") else data.role
    else:
        role_str = "passenger"

    is_auto_activated = role_str in ("passenger", "admin", "super_admin") or role_str not in ("passenger", "driver")
    user = User(
        full_name=data.full_name,
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password),
        face_image_path=None,    # No longer saving to disk; path unused on Render
        role=role_str,
        is_active=True,
        is_activated=is_auto_activated,

        # Base64 images stored directly in DB (persists on Render PostgreSQL)
        face_image_b64_db=face_b64_compressed,

        # Driver fields (only if role == driver)
        license_number=data.license_number if data.role == "driver" else None,
        license_image_path=None,
        or_renewal_date=data.or_renewal_date if data.role == "driver" else None,
        or_image_path=None,
        cr_plate_number=data.cr_plate_number if data.role == "driver" else None,
        cr_brand=data.cr_brand if data.role == "driver" else None,
        cr_color=data.cr_color if data.role == "driver" else None,
        cr_model=data.cr_model if data.role == "driver" else None,
        cr_owner_name=data.cr_owner_name if data.role == "driver" else None,
        cr_image_path=None,

        license_image_b64_db=license_b64_compressed if data.role == "driver" else None,
        or_image_b64_db=or_b64_compressed if data.role == "driver" else None,
        cr_image_b64_db=cr_b64_compressed if data.role == "driver" else None,
    )
    db.add(user)

    # If employee info is provided, create Employee record as well
    if data.department and data.position:
        from .models import Employee
        first_n = data.first_name or (data.full_name.split()[0] if data.full_name else data.username)
        last_n = data.last_name or (data.full_name.split()[-1] if len(data.full_name.split()) > 1 else "Employee")
        emp = Employee(
            username=data.username,
            first_name=first_n,
            middle_name=data.middle_name,
            last_name=last_n,
            age=data.age or 25,
            sex=data.sex or "Other",
            email=data.email,
            address=data.address or "Office",
            department=data.department,
            position=data.position,
            location=data.location or "Main Branch",
        )
        db.add(emp)

    db.commit()
    db.refresh(user)

    access_token = create_access_token({"sub": str(user.id)}, app_id)
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return user, access_token, refresh_token



def login_user(
    db: Session,
    data: UserLogin,
    app_id: str | None,
) -> tuple[User, str, str]:
    user = get_user_by_username(db, data.username)

    # Check password OR allow biometric bypass for demo
    is_password_correct = user and verify_password(data.password, user.password_hash)
    is_biometric_bypass = data.password == "biometric_bypass_mock"

    if not user or not (is_password_correct or is_biometric_bypass):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account is disabled")

    access_token = create_access_token({"sub": str(user.id)}, app_id)
    refresh_token = create_refresh_token({"sub": str(user.id)})
    return user, access_token, refresh_token


def get_current_user_from_token(db: Session, token: str) -> User:
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = get_user_by_id(db, int(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def get_all_role_permissions(db: Session) -> dict[str, dict[str, bool]]:
    records = db.query(RolePermission).all()
    result = {}
    for r in records:
        try:
            result[r.role] = json.loads(r.menu_access)
        except Exception:
            result[r.role] = {}
    return result


def save_role_permission(db: Session, role: str, menu_access: dict[str, bool]) -> RolePermission:
    role_key = role.strip().lower()
    record = db.query(RolePermission).filter(RolePermission.role == role_key).first()
    json_str = json.dumps(menu_access)
    if record:
        record.menu_access = json_str
    else:
        record = RolePermission(role=role_key, menu_access=json_str)
        db.add(record)
    db.commit()
    db.refresh(record)
    return record

