from sanic import Request, Unauthorized

from api import security


async def auth_middleware(request: Request):
    if request.path.startswith(("/admin", "/users")):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise Unauthorized("Authorization header missing or invalid")

        token = auth_header.split(" ")[1]
        user_data = security.verify_token(token, request.app.config.SECRET_KEY)

        if request.path.startswith("/admin") and not user_data.get("is_admin"):
            raise Unauthorized("Admin privileges required")

        request.ctx.user = user_data
