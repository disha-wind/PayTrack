from pydantic import ValidationError
from sanic import Blueprint, response, Request

from api.model import PaymentRequest
from api.security import generate_signature

payment_bp = Blueprint("payment_bp")


@payment_bp.post("/webhook/payment")
async def payment_webhook(request: Request):
    try:
        data = PaymentRequest(**request.json)

        expected_signature = generate_signature(
            {
                "account_id": data.account_id,
                "amount": str(data.amount),
                "transaction_id": data.transaction_id,
                "user_id": data.user_id
            },
            request.app.config.SECRET_KEY
        )

        if data.signature != expected_signature:
            return response.json({"error": "Invalid signature"}, status=400)

        # TODO: update data in database

        return response.json({"message": "Payment processed successfully"}, status=200)

    except ValidationError as e:
        return response.json({"error": e.errors()}, status=400)
    except Exception as e:
        return response.json({"error": str(e)}, status=500)
