from flask import Flask
from config import Config
from extensions import db, jwt
from routes.routes import user_bp
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)

# Configurar Swagger con autenticación JWT
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Mi API",
        "description": "Documentación de mi API",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "BearerAuth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Token JWT. Ejemplo: Bearer <tu_token>"
        }
    }
}

swagger = Swagger(app, template=swagger_template)

app.config.from_object(Config)

# CORS
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://main.d3k6p6uc1d4nx2.amplifyapp.com"
    ]
}}, supports_credentials=True)

# Extensiones
db.init_app(app)
jwt.init_app(app)

# Rutas
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return "API funcionando"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
