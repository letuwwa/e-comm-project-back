from flask import Blueprint, request
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db
from app.models import User, TokenBlocklist
from flask_jwt_extended import (
    get_jwt,
    jwt_required,
    get_jwt_identity,
    create_access_token,
    create_refresh_token,
)


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return {"msg": "invalid input"}, 400

    if User.query.filter_by(email=data["email"]).first():
        return {"msg": "email already exists"}, 400

    user = User(
        email=data["email"],
        password_hash=generate_password_hash(data["password"]),
    )

    db.session.add(user)
    db.session.commit()

    return {"msg": "user created"}, 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return {"msg": "invalid input"}, 400

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not check_password_hash(user.password_hash, data["password"]):
        return {"msg": "bad credentials"}, 401

    return {
        "access_token": create_access_token(identity=str(user.id)),
        "refresh_token": create_refresh_token(identity=str(user.id)),
    }, 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return {
        "access_token": create_access_token(identity=get_jwt_identity()),
    }, 200


@bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    token = TokenBlocklist(
        jti=get_jwt()["jti"],
        created_at=datetime.now(timezone.utc),
    )

    db.session.add(token)
    db.session.commit()

    return {"msg": "access token revoked"}, 200


@bp.route("/logout/refresh", methods=["POST"])
@jwt_required(refresh=True)
def logout_refresh():
    token = TokenBlocklist(
        jti=get_jwt()["jti"],
        created_at=datetime.now(timezone.utc),
    )

    db.session.add(token)
    db.session.commit()

    return {"msg": "refresh token revoked"}, 200