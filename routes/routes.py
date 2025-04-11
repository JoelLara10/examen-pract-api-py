from flask import Blueprint
from controllers.user_controller import login, get_users, create_user, update_user, delete_user
from models.user import User, db
from flask_jwt_extended import jwt_required
from flask import jsonify


user_bp = Blueprint("user_bp", __name__)

user_bp.route("/login", methods=["POST"])(login)
user_bp.route("/users", methods=["GET"])(get_users)
user_bp.route("/users", methods=["POST"])(create_user)
user_bp.route("/users/<int:id>", methods=["PUT"])(update_user)
user_bp.route("/users/<int:id>", methods=["DELETE"])(delete_user)
@user_bp.route('/seed', methods=['POST'])
def seed():
    if User.query.filter_by(email="admin@example.com").first():
        return jsonify({"msg": "Ya existe"}), 400

    user = User(name="Admin", email="admin@example.com")
    user.set_password("123456")  # 👈 ¡contraseña segura y hasheada!
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado"}), 201
