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
          application/json: { "token": "jwt_token" }
      401:
        description: Credenciales inválidas
    """
    data = request.get_json()
    print("Login recibido:", data)

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"msg": "Email y contraseña son requeridos"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        print("Credenciales inválidas")
        return jsonify({"msg": "Credenciales inválidas"}), 401

    access_token = create_access_token(identity=str(user.id))
    
    # Cambiamos el nombre de la propiedad a `token` para que el frontend la entienda
    return jsonify(token=access_token), 200


@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


@jwt_required()
def create_user():
    data = request.get_json()

    if not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({"error": "Faltan campos requeridos"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "Email ya registrado"}), 400

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
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: Usuario actualizado
      400:
        description: Email ya registrado
      404:
        description: Usuario no encontrado
    """
    data = request.json
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    new_email = data.get('email')
    if new_email and new_email != user.email:
        # Verifica que el nuevo email no esté en uso por otro usuario
        if User.query.filter_by(email=new_email).first():
            return jsonify({"error": "Email already exists"}), 400
        user.email = new_email

    user.name = data.get('name', user.name)

    if data.get('password'):
        user.set_password(data['password'])

    db.session.commit()
    return jsonify(user.to_dict()), 200



@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Usuario eliminado"}), 200
