import datetime
import hashlib
import hmac
import json

from config import COOKIE_KEY, PASSWORD_HMAC_KEY
from database import db
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from utils import abe, gen_token
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

app.config["SECRET_KEY"] = COOKIE_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    print(e)
    return "", 400


@app.route("/", methods=["GET"])
def hello():
    return redirect("/api/login")


@app.route("/api/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/api/login")


@app.route("/api/change", methods=["GET", "POST"])
def change_password():
    session.clear()
    if request.method == "GET":
        return render_template("change_password.html")
    else:
        username = request.json["username"]
        password = request.json["password"]
        new_password = request.json["new_password"]

        hashed_password = hmac.new(
            bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
        ).hexdigest()

        user = db.query(
            "SELECT id FROM users WHERE username = %s AND password = %s",
            (username, hashed_password),
        )

        if len(user) == 1:
            hashed_password = hmac.new(
                bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(new_password, "utf-8"), digestmod=hashlib.sha256
            ).hexdigest()

            if db.update("UPDATE users SET password = ? WHERE id = ?", (hashed_password, user[0]["id"])):
                return "", 200
            return "", 400

        else:
            return "Wrong username or password", 401


@app.route("/api/login", methods=["GET", "POST"])
def login():
    if "data" in session:
        if "ADMIN" in session["data"]["attributes"]["ROLES"]:
            return redirect("/api/register")
        else:
            return "", 200

    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]

        hashed_password = hmac.new(
            bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
        ).hexdigest()

        user = db.query(
            "SELECT id, attributes FROM users WHERE username = %s AND password = %s",
            (username, hashed_password),
        )

        if len(user) != 1:
            return "Wrong username or password", 401

        user[0]["attributes"] = json.loads(user[0]["attributes"])
        session["data"] = user[0]

        if "ADMIN" in session["data"]["attributes"]["ROLES"]:
            return redirect("/api/register")
        return "", 200

    return render_template("login.html")


@app.route("/api/register", methods=["POST", "GET"])
def register():
    if "data" not in session:
        return redirect("/")

    if "ADMIN" not in session["data"]["attributes"]["ROLES"]:
        return "", 403

    if request.method == "POST":
        username = request.json["username"]
        password = request.json["password"]

        attributes = {}
        for attr, vals in request.json["attributes"].items():
            attributes[attr.upper()] = [val.upper() for val in vals]

        user = db.query("SELECT COUNT(1) AS cnt FROM users WHERE username = %s", (username,))

        hashed_password = hmac.new(
            bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
        ).hexdigest()

        if user[0]["cnt"] != 0:
            return "Username already exists", 409
        db.update(
            "INSERT INTO users(username, password, attributes) VALUES (%s, %s, %s)",
            (username, hashed_password, json.dumps(attributes)),
        )
        return "", 200

    return render_template("register.html")


@app.route("/api/parameters", methods=["GET"])
def parameters():
    if not request.cookies.get("session") or not session["data"]:
        return "", 401

    abe_attributes = []
    for attr, vals in session["data"]["attributes"].items():
        for val in vals:
            abe_attributes.append(attr + "@" + val)

    dict_param = {
        "token": gen_token(
            {
                "uid": session["data"]["id"],
                "attributes": session["data"]["attributes"],
                "exp": datetime.datetime.now(tz=datetime.timezone.utc).timestamp() + 3600,
            }
        ),
        "public_key": abe.get_public_key().decode(),
        "secret_key": abe.gen_secret_key(abe_attributes).decode(),
    }

    return dict_param, 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run("0.0.0.0", 2808)
