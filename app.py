from flask import Flask, request
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
import sqlite3
import bcrypt

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token:
            return {"error": "Token ausente"}, 401

        try:
            jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return {"error": "Token inválido"}, 401

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return {"message": "API JWT funcionando"}


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(force=True, silent=True)

    if not data:
        return {"error": "JSON inválido"}, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "email e password são obrigatórios"}, 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    try:
        cursor.execute(
            "INSERT INTO users (email, password) VALUES (?, ?)",
            (email, hashed_password)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return {"error": "Usuário já existe"}, 400

    conn.close()
    return {"message": "Usuário criado com sucesso"}, 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True, silent=True)

    if not data:
        return {"error": "JSON inválido"}, 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {"error": "email e password são obrigatórios"}, 400

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )
    user = cursor.fetchone()
    conn.close()

    if not user:
        return {"error": "Email ou senha inválidos"}, 401
    stored_password = user [2]
    if not bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8")):
        return {"error": "Email ou senha invalidos"}, 401


    token = jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return {"token": token}, 200


@app.route("/perfil", methods=["GET"])
@token_required
def perfil():
    return {"message": "Você acessou uma rota protegida"}, 200


if __name__ == "__main__":
    app.run(debug=True)

