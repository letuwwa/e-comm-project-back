from __future__ import annotations

from uuid import UUID
from typing import Any
from flask import Request
from datetime import UTC, datetime

from app.extensions import db
from app.models import Product, TokenBlocklist


def get_json_data(request: Request) -> dict[str, Any]:
    return request.get_json(silent=True) or {}


def serialize_product(
    product: Product, *, include_description: bool = False
) -> dict[str, Any]:
    payload = {
        "id": str(product.id),
        "name": product.name,
        "price": float(product.price),
    }

    if include_description:
        payload["description"] = product.description

    return payload


def get_user_product(*, product_id: UUID, user_id: str) -> Product | None:
    return Product.query.filter_by(id=product_id, user_id=user_id).first()


def revoke_token(jti: str) -> None:
    db.session.add(
        TokenBlocklist(
            jti=jti,
            created_at=datetime.now(UTC),
        )
    )
    db.session.commit()
