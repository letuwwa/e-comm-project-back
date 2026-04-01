import uuid6
from datetime import datetime, UTC
from sqlalchemy.dialects.postgresql.base import UUID

from .extensions import db


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    is_active = db.Column(db.Boolean, default=True)


class User(BaseModel):
    __tablename__ = 'users'

    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    products = db.relationship("Product", back_populates="user", lazy=True)


class Product(BaseModel):
    __tablename__ = 'products'

    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="products")


class TokenBlocklist(db.Model):
    __tablename__ = "token_blocklist"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid6.uuid7,
    )

    jti = db.Column(db.String, nullable=False, index=True)

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )