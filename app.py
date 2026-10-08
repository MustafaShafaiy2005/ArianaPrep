from flask import Flask, session, send_from_directory

from database import init_db, get_db
from routes.auth import auth_bp


app = Flask(__name__)

app.secret_key = "dev-secret-key-change-later"

app.register_blueprint(auth_bp)


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/login")
def login_page():
    return send_from_directory("frontend", "login.html")


@app.route("/register")
def register_page():
    return send_from_directory("frontend", "register.html")


@app.route("/dashboard")
def dashboard_page():
    return send_from_directory("frontend", "dashboard.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)


@app.route("/api/health")
def health():
    connection = get_db()

    result = connection.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    ).fetchall()

    connection.close()

    tables = [row["name"] for row in result]

    return {
        "status": "ok",
        "database": "connected",
        "tables": tables
    }


if __name__ == "__main__":
    init_db()
    app.run(debug=True)