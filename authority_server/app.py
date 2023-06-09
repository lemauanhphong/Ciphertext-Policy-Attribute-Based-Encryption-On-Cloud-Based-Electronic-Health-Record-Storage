import datetime
import hashlib
import hmac

from config import COOKIE_KEY, PASSWORD_HMAC_KEY
from database import db
from flask import Flask, request, session
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
    return "Hello world"


@app.route("/api/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    hashed_password = hmac.new(
        bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    user = db.query(
        "SELECT id, attributes FROM users WHERE username = %s AND password = %s",
        (username, hashed_password),
    )

    if len(user) != 1:
        return "Wrong username or password", 401

    user[0]["attributes"] = user[0]["attributes"].split(",")
    session["data"] = user[0]

    return "", 200


@app.route("/api/register", methods=["POST"])
def register():
    if not request.cookies.get("session") or not session["data"]:
        return "", 401

    if "admin" not in session["data"]["attributes"]:
        return "", 403

    username = request.form["username"]
    password = request.form["password"]
    attributes = request.form["attributes"]

    user = db.query("SELECT COUNT(1) AS cnt FROM users WHERE username = %s", (username,))

    hashed_password = hmac.new(
        bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
    ).hexdigest()

    if user[0]["cnt"] != 0:
        return "Username already exists", 409

    db.update(
        "INSERT INTO users(username, password, attributes) VALUES (%s, %s, %s)", (username, hashed_password, attributes)
    )
    return "", 200


@app.route("/api/parameters", methods=["GET"])
def parameters():
    if not request.cookies.get("session") or not session["data"]:
        return "", 401

    dict_param = {
        "token": gen_token(
            {
                "uid": session["data"]["id"],
                "attributes": session["data"]["attributes"],
                "exp": datetime.datetime.now(tz=datetime.timezone.utc).timestamp() + 3600,
            }
        ),
        "public_key": abe.get_public_key().decode(),
        "secret_key": abe.gen_secret_key(session["data"]["attributes"]).decode(),
    }

    return dict_param, 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(port=2808, debug=True)
