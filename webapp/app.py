from flask import Blueprint, Flask
from flask_restful import Api
from resources.Steam import Steam

import os

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Steam, '/steam')

def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)
    
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


if __name__ == "__main__":
    app = create_app(__name__)
    app.run(host='0.0.0.0',port=int(os.environ['PORT']), debug=True)
