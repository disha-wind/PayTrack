from .auth import auth_bp
from .users import users_bp
from .admin import admin_bp
from .payment import payment_bp

def register_routes(app):
    app.blueprint(auth_bp)
    app.blueprint(users_bp)
    app.blueprint(admin_bp)
    app.blueprint(payment_bp)
