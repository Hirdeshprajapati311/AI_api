from flask import Flask

from app.routes.airoutes import ai_routes
from app.database.mongodb import init_db
from app.routes.routes import new_routes
from app.routes.new_routes import ai_new_routes

app = Flask(__name__)
init_db()
app.register_blueprint(ai_routes)
app.register_blueprint(new_routes)
app.register_blueprint(ai_new_routes)



