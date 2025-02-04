import os

from pydantic import BaseModel, EmailStr, ValidationError
from sanic import Sanic, Request, response

from api import security
from database.model import Admin, User
from database.unit import Database

app = Sanic("PayTrack")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
@app.before_server_start
async def setup_config(application, loop):
    application.config.SECRET_KEY = os.getenv("SECRET_KEY")
    
@app.before_server_start
async def setup_database(application, loop):
    application.ctx.db = Database()
    await application.ctx.db.init()

@app.after_server_stop
async def close_database(application, loop):
    await application.ctx.db.close()

@app.post("/auth/login")
async def auth_login(request: Request):
    try:
        data = LoginRequest(**request.json)
        user: User = await app.ctx.db.get_by_email(data.email)
        
        if not user:
            return response.json({"error": "User not found"}, status=404)
        if not security.verify_password(data.password, user.password_hash):
            return response.json({"error": "Invalid password"}, status=401)
        
        is_admin = await app.ctx.db.get_by_id(Admin, user.id)
        token = security.create_access_token(
            {
                "email": data.email, 
                "is_admin": is_admin
            },
            app.config.SECRET_KEY
        )
        return response.json(
            {
                "message": "Login successful",  
                "token": token
            }
        )
    except ValidationError as e:
        return response.json({"error": e.errors()}, status=400)
    