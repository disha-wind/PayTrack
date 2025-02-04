from sanic import Blueprint, response, Request

from database.model import User

users_bp = Blueprint("users", url_prefix="/users")

@users_bp.get("/me")
async def get_user_info(request: Request):
    user = await request.app.ctx.db.get_by_id(User, request.ctx.user["id"])
    if user:
        return response.json(
            {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name
            }
        )
    return response.json({"error": "User not found"}, status=404)