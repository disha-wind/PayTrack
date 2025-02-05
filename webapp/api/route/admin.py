from sanic import Blueprint

from api.route.everyone import get_user_info


admin_bp = Blueprint("admin", url_prefix="/admin")
admin_bp.add_route(get_user_info, "/me")


@admin_bp.post("/users")
async def create_user(request):
    pass

@admin_bp.get("/users")
async def get_users(request):
    pass

@admin_bp.get("/users/<user_id:int>")
async def get_user(request, user_id):
    pass

@admin_bp.put("/users/<user_id:int>")
async def update_user(request, user_id):
    pass

@admin_bp.delete("/users/<user_id:int>")
async def delete_user(request, user_id):
    pass

@admin_bp.get("/users/<user_id:int>/accounts")
async def get_accounts(request, user_id):
    pass
