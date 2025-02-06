from pydantic import ValidationError
from sanic import Blueprint, response

from api import security
from api.model import AddUserRequest, UpdateUserRequest
from api.route.everyone import get_user_info
from api.security import hash_password
from database.model import User

admin_bp = Blueprint("admin", url_prefix="/admin")
admin_bp.add_route(get_user_info, "/me")


@admin_bp.post("/users")
async def create_user(request):
    try:
        data = AddUserRequest(**request.json)
        user = User(
            id=data.id,
            email=data.email,
            password_hash=security.hash_password(data.password),
            full_name=data.full_name
        )
        await request.app.ctx.db.add(user)
        user = await request.app.ctx.db.get_by_id(User, data.id)
        return response.json(user.to_dict(exclude=["password_hash"]), status=201)
    except ValidationError as e:
        return response.json({"error": e.errors()}, status=400)

@admin_bp.get("/users")
async def get_users(request):
    users = await request.app.ctx.db.get_all(User)
    return response.json([user.to_dict(exclude=["password_hash"]) for user in users])

@admin_bp.get("/users/<user_id:int>")
async def get_user(request, user_id):
    user = await request.app.ctx.db.get_by_id(User, user_id)
    if not user:
        return response.json({"error": "User not found"}, status=404)
    return response.json(user.to_dict(exclude=["password_hash"]))

@admin_bp.put("/users/<user_id:int>")
async def update_user(request, user_id):
    try:
        data = UpdateUserRequest(**request.json)

        user = await request.app.ctx.db.get_by_id_with_session(User, user_id)
        if not user:
            return response.json({"message": "User not found"}, status=404)
        
        if data.id:
            user.id = data.id
        if data.email:
            user.email = data.email
        if data.password:
            user.password_hash = hash_password(data.password)
        if data.full_name:
            user.full_name = data.full_name
        
        await request.app.ctx.db.commit()

        return response.json({"message": "User updated successfully"}, status=200)

    except ValidationError as e:
        return response.json({"error": e.errors()}, status=400)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)


@admin_bp.delete("/users/<user_id:int>")
async def delete_user(request, user_id):
    try:
        await request.app.ctx.db.remove_by_id(User, user_id)
    except ValueError as e:
        return response.json({"error": str(e)}, status=404)
    return response.json({"message": "User deleted"})

@admin_bp.get("/users/<user_id:int>/accounts")
async def get_accounts(request, user_id):
    accounts = await request.app.ctx.db.get_accounts(user_id)
    return response.json([account.to_dict() for account in accounts])
