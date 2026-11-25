import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column
from typing import ClassVar
from ..database import Base
from datetime import datetime, timezone, timedelta

MANILA_TZ = timezone(timedelta(hours=8))

def manila_now():
    return datetime.now(MANILA_TZ).replace(tzinfo=None)


class User(Base):
    __tablename__ = "auth_users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    full_name: Mapped[str] = mapped_column(sa.String(120))
    username: Mapped[str] = mapped_column(sa.String(80), unique=True, index=True)
    email: Mapped[str] = mapped_column(sa.String(200), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(sa.String(255))
    face_image_path: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    role: Mapped[str] = mapped_column(sa.String(100), default="passenger")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_activated: Mapped[bool] = mapped_column(default=False)
    balance: Mapped[float] = mapped_column(sa.Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=manila_now)

    # Driver Verification fields
    license_number: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    license_image_path: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    or_renewal_date: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    or_image_path: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    cr_plate_number: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    cr_brand: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    cr_color: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    cr_model: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    cr_owner_name: Mapped[str | None] = mapped_column(sa.String(120), nullable=True)
    cr_image_path: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)

    # Base64 image storage — stored directly in DB so images persist on Render.
    # Render's filesystem is ephemeral; PostgreSQL TEXT columns handle base64 fine.
    face_image_b64_db: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    license_image_b64_db: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    or_image_b64_db: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    cr_image_b64_db: Mapped[str | None] = mapped_column(sa.Text, nullable=True)

    @property
    def face_image_base64(self) -> str | None:
        return self.face_image_b64_db

    @property
    def license_image_base64(self) -> str | None:
        return self.license_image_b64_db

    @property
    def or_image_base64(self) -> str | None:
        return self.or_image_b64_db

    @property
    def cr_image_base64(self) -> str | None:
        return self.cr_image_b64_db


class Booking(Base):
    __tablename__ = "ride_bookings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    passenger_id: Mapped[int] = mapped_column(sa.ForeignKey("auth_users.id"))
    driver_id: Mapped[int | None] = mapped_column(sa.ForeignKey("auth_users.id"), nullable=True)
    status: Mapped[str] = mapped_column(sa.String(20), default="pending") # pending, accepted, completed, cancelled
    pickup_lat: Mapped[float] = mapped_column(sa.Float)
    pickup_lng: Mapped[float] = mapped_column(sa.Float)
    dropoff_lat: Mapped[float] = mapped_column(sa.Float)
    dropoff_lng: Mapped[float] = mapped_column(sa.Float)
    pickup_address: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    dropoff_address: Mapped[str | None] = mapped_column(sa.String(500), nullable=True)
    amount: Mapped[float | None] = mapped_column(sa.Float, nullable=True, default=0.0)
    document_image: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    document_info: Mapped[str | None] = mapped_column(sa.String(1000), nullable=True)
    document_tip: Mapped[str | None] = mapped_column(sa.String(1000), nullable=True)
    received_image: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    signature_image: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=manila_now)


class BalanceLog(Base):
    __tablename__ = "auth_balance_logs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("auth_users.id"))
    created_by_id: Mapped[int] = mapped_column(sa.ForeignKey("auth_users.id"))
    amount: Mapped[float] = mapped_column(sa.Float)
    new_balance: Mapped[float] = mapped_column(sa.Float)
    reference_number: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    payment_method: Mapped[str | None] = mapped_column(sa.String(50), nullable=True)
    status: Mapped[str] = mapped_column(sa.String(30), default="approved")
    created_at: Mapped[datetime] = mapped_column(default=manila_now)

    # Relationships to fetch usernames easily
    user = sa.orm.relationship("User", foreign_keys=[user_id])
    created_by = sa.orm.relationship("User", foreign_keys=[created_by_id])


class Employee(Base):
    __tablename__ = "employees"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str | None] = mapped_column(sa.String(80), nullable=True)
    first_name: Mapped[str] = mapped_column(sa.String(100))
    middle_name: Mapped[str | None] = mapped_column(sa.String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(sa.String(100))
    age: Mapped[int] = mapped_column(sa.Integer)
    sex: Mapped[str] = mapped_column(sa.String(20))
    email: Mapped[str] = mapped_column(sa.String(200))
    address: Mapped[str] = mapped_column(sa.String(500))
    department: Mapped[str] = mapped_column(sa.String(100))
    position: Mapped[str] = mapped_column(sa.String(100))
    location: Mapped[str] = mapped_column(sa.String(200))
    created_at: Mapped[datetime] = mapped_column(default=manila_now)


class RolePermission(Base):
    __tablename__ = "auth_role_permissions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    role: Mapped[str] = mapped_column(sa.String(100), unique=True, index=True)
    menu_access: Mapped[str] = mapped_column(sa.Text) # JSON string representation of dict: {"employee_list": true, ...}
    updated_at: Mapped[datetime] = mapped_column(default=manila_now, onupdate=manila_now)


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int | None] = mapped_column(sa.ForeignKey("auth_users.id"), nullable=True)
    user_name: Mapped[str] = mapped_column(sa.String(150))
    user_role: Mapped[str] = mapped_column(sa.String(50), default="Passenger")
    topic: Mapped[str] = mapped_column(sa.String(200), default="General Support")
    message_snippet: Mapped[str | None] = mapped_column(sa.Text, nullable=True)
    status: Mapped[str] = mapped_column(sa.String(30), default="waiting") # waiting, active, resolved
    agent_id: Mapped[int | None] = mapped_column(sa.ForeignKey("auth_users.id"), nullable=True)
    agent_name: Mapped[str | None] = mapped_column(sa.String(150), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=manila_now)
    updated_at: Mapped[datetime] = mapped_column(default=manila_now, onupdate=manila_now)
    claimed_at: Mapped[datetime | None] = mapped_column(sa.DateTime, nullable=True)
    resolved_at: Mapped[datetime | None] = mapped_column(sa.DateTime, nullable=True)

    messages = sa.orm.relationship("SupportMessage", back_populates="ticket", cascade="all, delete-orphan")


class SupportMessage(Base):
    __tablename__ = "support_messages"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ticket_id: Mapped[int] = mapped_column(sa.ForeignKey("support_tickets.id"))
    sender_type: Mapped[str] = mapped_column(sa.String(20)) # user, agent
    sender_name: Mapped[str] = mapped_column(sa.String(150))
    text: Mapped[str] = mapped_column(sa.Text)
    created_at: Mapped[datetime] = mapped_column(default=manila_now)

    ticket = sa.orm.relationship("SupportTicket", back_populates="messages")


