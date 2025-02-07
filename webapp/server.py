import os

from sanic import Sanic
from sanic_ext import Extend

from api.middleware import auth_middleware
from api.route import register_routes
from database.unit import Database

app = Sanic("PayTrack")
Extend(app)
app.ext.openapi.describe(
    title="PayTrack API",
    version="0.0.1",
    description="API documentation for PayTrack"
)

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


if __name__ == '__main__':
    app.middleware('request')(auth_middleware)
    register_routes(app)
    app.run(host='0.0.0.0', port=8000, single_process=True)