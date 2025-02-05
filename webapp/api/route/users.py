from sanic import Blueprint, Request

from api.route.everyone import get_user_info


users_bp = Blueprint("users", url_prefix="/users")
users_bp.add_route(get_user_info, "/me")

@users_bp.get("/me/accounts")
async def get_accounts(request: Request):
    pass

@users_bp.get("/me/payments")
async def get_payments(request: Request):
    pass
