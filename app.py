from flask import Flask
from config import Config
from extensions import db, jwt, swagger
from routes.routes import user_bp
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)
CORS(app, resources={r"/*": {
    "origins": [
        "http://localhost:3000",
        "https://main.d3k6p6uc1d4nx2.amplifyapp.com"
    ]
}}, supports_credentials=True)

db.init_app(app)
jwt.init_app(app)
swagger.init_app(app)

app.register_blueprint(user_bp)

@app.route('/')
def home():
    return "API funcionando"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
