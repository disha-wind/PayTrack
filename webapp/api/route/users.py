from sanic import Blueprint, Request, response

from api.route.everyone import get_user_info

users_bp = Blueprint("users", url_prefix="/users")
users_bp.add_route(get_user_info, "/me")

@users_bp.get("/me/accounts")
async def get_accounts(request: Request):
    accounts = await request.app.ctx.db.get_accounts(request.ctx.user["id"])
    if accounts:
        return response.json(
            [
                {
                    "id": account.id,
                    "balance": str(account.balance)
                }
                for account in accounts
            ]
        )
    return response.json([])

@users_bp.get("/me/payments")
async def get_payments(request: Request):
    payments = await request.app.ctx.db.get_payments(request.ctx.user["id"])
    if payments:
        return response.json(
            [
                {
                    "transaction_id": payment.transaction_id,
                    "amount": str(payment.amount)
                }
                for payment in payments
            ]
        )
    return response.json([])
