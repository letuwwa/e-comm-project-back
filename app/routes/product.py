import uuid
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.api import get_json_data, get_user_product, serialize_product
from app.extensions import db
from app.models import Product


bp = Blueprint("product", __name__)


@bp.route("/products", methods=["POST"])
@jwt_required()
def create_product():
    data = get_json_data(request)
    user_id = get_jwt_identity()

    product = Product(
        name=data["name"],
        price=data["price"],
        description=data["description"],
        user_id=user_id,
    )

    db.session.add(product)
    db.session.commit()

    return {"message": "Product created"}, 201


@bp.route("/products", methods=["GET"])
@jwt_required()
def get_my_products():
    user_id = get_jwt_identity()
    products = Product.query.filter_by(user_id=user_id).all()

    return [serialize_product(product) for product in products]


@bp.route("/products/<uuid:product_id>", methods=["GET"])
@jwt_required()
def get_product(product_id: uuid.UUID):
    user_id = get_jwt_identity()

    product = get_user_product(product_id=product_id, user_id=user_id)

    if not product:
        return {"error": "Not found"}, 404

    return serialize_product(product, include_description=True)


@bp.route("/products/<uuid:product_id>", methods=["PUT"])
@jwt_required()
def update_product(product_id: uuid.UUID):
    user_id = get_jwt_identity()
    data = get_json_data(request)

    product = get_user_product(product_id=product_id, user_id=user_id)

    if not product:
        return {"error": "Not found"}, 404

    product.name = data.get("name", product.name)
    product.price = data.get("price", product.price)
    product.description = data.get("description", product.description)

    db.session.commit()

    return {"message": "Updated"}


@bp.route("/products/<uuid:product_id>", methods=["DELETE"])
@jwt_required()
def delete_product(product_id: uuid.UUID):
    user_id = get_jwt_identity()

    product = get_user_product(product_id=product_id, user_id=user_id)

    if not product:
        return {"error": "Not found"}, 404

    db.session.delete(product)
    db.session.commit()

    return {"message": "Deleted"}
