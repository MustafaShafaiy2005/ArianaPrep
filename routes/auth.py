from flask import Blueprint, request, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import get_db


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return {
            "error": "Name, email, and password are required."
        }, 400

    password_hash = generate_password_hash(password)

    connection = get_db()

    try:
        connection.execute(
            """
            INSERT INTO users (name, email, password)
            VALUES (?, ?, ?)
            """,
            (name, email, password_hash)
        )

        connection.commit()

    except Exception:
        connection.close()

        return {
            "error": "An account with this email may already exist."
        }, 400

    connection.close()

    return {
        "message": "Account created successfully!"
    }, 201


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return {
            "error": "Email and password are required."
        }, 400

    connection = get_db()

    user = connection.execute(
        """
        SELECT id, name, email, password
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    if user is None:
        return {
            "error": "Invalid email or password."
        }, 401

    if not check_password_hash(user["password"], password):
        return {
            "error": "Invalid email or password."
        }, 401

    session["user_id"] = user["id"]

    return {
        "message": "Login successful!",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }, 200


@auth_bp.route("/api/me", methods=["GET"])
def current_user():
    user_id = session.get("user_id")

    if not user_id:
        return {
            "error": "Not logged in."
        }, 401

    connection = get_db()

    user = connection.execute(
        """
        SELECT id, name, email
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    if user is None:
        session.clear()

        return {
            "error": "User not found."
        }, 401

    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }, 200


@auth_bp.route("/api/logout", methods=["POST"])
def logout():
    session.clear()

    return {
        "message": "Logged out successfully!"
    }, 200