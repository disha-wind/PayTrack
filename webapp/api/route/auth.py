from pydantic import ValidationError
from sanic import Request, Blueprint, response

from api import security
from api.model import LoginRequest
from database.model import User, Admin

auth_bp = Blueprint("auth", url_prefix="/auth")

@auth_bp.post("/login")
async def auth_login(request: Request):
    try:
        data = LoginRequest(**request.json)
        user: User = await request.app.ctx.db.get_by_email(data.email)

        if not user:
            return response.json({"error": "User not found"}, status=404)
        if not security.verify_password(data.password, user.password_hash):
            return response.json({"error": "Invalid password"}, status=401)

        is_admin = await request.app.ctx.db.get_by_id(Admin, user.id)
        token = security.create_access_token(
            {
                "id": user.id,
                "email": user.email,
                "is_admin": is_admin is not None
            },
            request.app.config.SECRET_KEY
        )
        return response.json(
            {
                "message": "Login successful",
                "token": token,
                "token_type": "Bearer"
            }
        )
    except ValidationError as e:
        return response.json({"error": e.errors()}, status=400)