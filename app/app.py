from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_cors import CORS
import os

from models import db
from app.routes.game_routes import bp


def create_app():
    app = Flask(__name__)
    CORS(app)

    handle_errors(app)


    load_dotenv()
    LOCAL_DB_URL = os.getenv('LOCAL_DB_URL') 

    app.config['SQLALCHEMY_DATABASE_URI'] = LOCAL_DB_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.register_blueprint(bp)
    db.init_app(app)
    
    with app.app_context():
        db.create_all()


    @app.route('/')
    def index():
        return "HOME PAGE HA"
    return app

def handle_errors(app):
    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({"error": str(error)}), 500

    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify(error=str(error.description)), 400
        return response