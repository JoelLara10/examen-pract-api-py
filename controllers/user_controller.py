from flask import request, jsonify
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token, jwt_required

def login():
    """
    Iniciar sesión
    ---
    tags:
      - Autenticación
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login exitoso
        examples:
          application/json: { "access_token": "token_jwt" }
      401:
        description: Credenciales inválidas
    """
    data = request.json
    user = User.query.filter_by(email=data.get('email')).first()
    if user and user.check_password(data.get('password')):
        token = create_access_token(identity=user.id)
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credentials"}), 401


@jwt_required()
def get_users():
    """
    Obtener todos los usuarios
    ---
    tags:
      - Usuarios
    responses:
      200:
        description: Lista de usuarios
    """
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@jwt_required()
def create_user():
    """
    Crear un nuevo usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - password
          properties:
            name:
              type: string
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuario creado
      400:
        description: Email ya registrado
    """
    data = request.json
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email already exists"}), 400
    user = User(name=data['name'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201


@jwt_required()
def update_user(id):
    """
    Actualizar usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: id
        required: true
        type: integer
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            password:
              type: string
    responses:
      200:
        description: Usuario actualizado
      404:
        description: Usuario no encontrado
    """
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.name = data.get('name', user.name)
    if data.get('password'):
        user.set_password(data['password'])
    db.session.commit()
    return jsonify(user.to_dict()), 200


@jwt_required()
def delete_user(id):
    """
    Eliminar usuario
    ---
    tags:
      - Usuarios
    parameters:
      - in: path
        name: id
        required: true
        type: integer
    responses:
      200:
        description: Usuario eliminado
      404:
        description: Usuario no encontrado
    """
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted"}), 200
