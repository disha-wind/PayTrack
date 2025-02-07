from sanic import Blueprint, Request, response
from sanic_ext.extensions.openapi import openapi

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

@users_bp.get("/me/accounts")
@openapi.response(
    200,
    {
        "application/json": {
            "example": [
                {
                    "id": "123",
                    "balance": "1000.50"
                },
                {
                    "id": "456",
                    "balance": "250.00"
                }
            ]
        }
    }
)
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
@openapi.response(
    200,
    {
        "application/json": {
            "example": [
                {
                    "transaction_id": "tx_789",
                    "amount": "500.00"
                },
                {
                    "transaction_id": "tx_101",
                    "amount": "120.75"
                }
            ]
        }
    }
)
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
