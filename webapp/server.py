import os

from sanic import Sanic

from api.middleware import auth_middleware
from api.route import register_routes
from database.unit import Database

app = Sanic("PayTrack")

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

app.middleware('request')(auth_middleware)
register_routes(app)