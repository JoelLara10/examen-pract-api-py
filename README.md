# 🛠️ API REST de Usuarios - Flask + MySQL (AWS)

Esta API permite realizar autenticación y gestión completa de usuarios. Está construida con **Flask**, conectada a una base de datos **MySQL en AWS RDS** y desplegada en una instancia **EC2**. Incluye documentación Swagger.

## 📌 Funcionalidades

- Login (`POST /login`)
- Obtener todos los usuarios (`GET /users`)
- Obtener usuario por ID (`GET /users/<id>`)
- Crear nuevo usuario (`POST /users`)
- Actualizar usuario (`PUT /users/<id>`)
- Eliminar usuario (`DELETE /users/<id>`)

## ⚙️ Tecnologías

- Python 3.10+
- Flask
- SQLAlchemy
- Flask-CORS
- PyMySQL
- Flasgger (Swagger UI)
- MySQL (RDS)
- EC2 (Amazon Linux)

Despliegue en EC2
Clonar el repositorio

Instalar dependencias:

pip install -r requirements.txt
Exportar variables del entorno:
export FLASK_APP=app.py

Iniciar la app:
python app.py
🧪 Swagger UI
Una vez levantada la API, puedes acceder a la documentación en:
http://<tu-ec2>:8000/apidocs/

📦 Instalación Local

pip install -r requirements.txt
python app.py

