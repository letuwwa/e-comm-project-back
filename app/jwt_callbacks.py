from app.extensions import db
from app.models import TokenBlocklist


def init_jwt_callbacks(jwt):
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]

        return db.session.query(
            db.exists().where(TokenBlocklist.jti == jti)
        ).scalar()