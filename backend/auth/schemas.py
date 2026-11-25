from __future__ import annotations
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional


class UserRegister(BaseModel):
    full_name: str
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    role: Optional[str] = "passenger"
    department: Optional[str] = None
    position: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    address: Optional[str] = None
    location: Optional[str] = None
    license_number: Optional[str] = None
    or_renewal_date: Optional[str] = None
    cr_plate_number: Optional[str] = None
    cr_brand: Optional[str] = None
    cr_color: Optional[str] = None
    cr_model: Optional[str] = None
    cr_owner_name: Optional[str] = None

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    @field_validator("username")
    @classmethod
    def username_valid(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters")
        if not v.replace("_", "").isalnum():
            raise ValueError("Username must be alphanumeric (underscores allowed)")
        return v.lower()


class RegisterRequest(BaseModel):
    user: UserRegister
    face_image: Optional[str] = None    # base64 data-URL from camera
    license_image: Optional[str] = None # base64 data-URL
    or_image: Optional[str] = None      # base64 data-URL
    cr_image: Optional[str] = None      # base64 data-URL
    app_id: Optional[str] = None


class UserLogin(BaseModel):
    username: str
    password: str
    face_image: Optional[str] = None


class UserOut(BaseModel):
    id: int
    full_name: str
    username: str
    email: str
    face_image_path: str | None = None
    is_active: bool
    is_activated: bool
    role: str
    balance: float = 0.0
    created_at: datetime

    # Driver documents metadata
    license_number: str | None = None
    license_image_path: str | None = None
    or_renewal_date: str | None = None
    or_image_path: str | None = None
    cr_plate_number: str | None = None
    cr_brand: str | None = None
    cr_color: str | None = None
    cr_model: str | None = None
    cr_owner_name: str | None = None
    cr_image_path: str | None = None

    # Base64 images returned to frontend (sourced from *_b64_db DB columns via router)
    face_image_base64: str | None = None
    license_image_base64: str | None = None
    or_image_base64: str | None = None
    cr_image_base64: str | None = None

    model_config = {"from_attributes": True}


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserOut


class RefreshRequest(BaseModel):
    refresh_token: str


class MessageResponse(BaseModel):
    message: str


class UpdateBalanceRequest(BaseModel):
    amount: float


class LoadBalanceGcashQrRequest(BaseModel):
    amount: float
    reference_number: str
    payment_method: Optional[str] = "gcash"


class EmployeeCreate(BaseModel):
    username: str
    password: str
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int
    sex: str
    email: EmailStr
    address: str
    department: str
    position: str
    location: str


class EmployeeOut(BaseModel):
    id: int
    username: Optional[str] = None
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    age: int
    sex: str
    email: str
    address: str
    department: str
    position: str
    location: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FixTopUpReferenceRequest(BaseModel):
    system_ref: str
    new_reference_number: str


class RolePermissionSave(BaseModel):
    role: str
    menu_access: dict[str, bool]


class RolePermissionOut(BaseModel):
    id: int
    role: str
    menu_access: dict[str, bool]
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


class CreateSupportTicket(BaseModel):
    user_name: str
    user_role: Optional[str] = "Passenger"
    topic: Optional[str] = "General Support"
    message: str
    user_id: Optional[int] = None


class SendSupportMessage(BaseModel):
    sender_type: str  # user or agent
    sender_name: str
    text: str


class ClaimSupportTicket(BaseModel):
    agent_name: str



