from flask import Blueprint
from app.api import serialize_product
from app.models import Product


index_bp = Blueprint("main", __name__)


@index_bp.route("/")
def index():
    products = Product.query.all()

    return [serialize_product(product) for product in products]
