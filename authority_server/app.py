import datetime
import hashlib
import hmac

from config import COOKIE_KEY, PASSWORD_HMAC_KEY
from database import db
from flask import Flask, request, session, redirect, render_template
from flask_session import Session
# from utils import abe, gen_token
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
    return redirect('/api/login')


@app.route("/api/login", methods=["GET", "POST"])
def login():
    if "data" in session:
        return redirect('/api/register')

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hmac.new(
            bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
        ).hexdigest()

        user = db.query(
            "SELECT id, username, role, permission FROM users WHERE username = %s AND password = %s",
            (username, hashed_password),
        )
        print(user)
        if len(user) != 1:
            return "Wrong username or password", 401
        session["data"] = user[0]
        return "", 200
    
    return render_template('login.html')


@app.route("/api/register", methods=["POST", "GET"])
def register():
    if "data" in session:
        return "", 401

    if session["data"]["role"] != "admin":
        return "", 403

    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        user = db.query("SELECT COUNT(1) AS cnt FROM users WHERE username = %s", (username,))

        hashed_password = hmac.new(
            bytes(PASSWORD_HMAC_KEY, "utf-8"), msg=bytes(password, "utf-8"), digestmod=hashlib.sha256
        ).hexdigest()

        if user[0]["cnt"] != 0:
            return 409, "Username already exists"
        db.update("INSERT INTO users(username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        return "", 200
    
    return render_template('register.html')


@app.route("/api/parameters", methods=["GET"])
def parameters():
    if not request.cookies.get("session") or not session["data"]:
        return "", 401

    # TODO: handle generating secret key with proper attributes
    dict_param = {}
    dict_param["token"] = gen_token(
        {
            "permission": session["data"]["permission"],
            "username": session["data"]["username"],
            "exp": datetime.datetime.now(tz=datetime.timezone.utc).timestamp() + 3600,
        }
    )
    dict_param["public_key"] = abe.get_public_key()

    # TODO: handle attributes
    # dict_param["secret_key"] = abe.gen_secret_key(attributes)

    # TODO: handle write permission
    # if session["data"]["permission"]:
    #    dict_param["encrypt_key"] = gen_encrypt_key()

    return dict_param, 200, {"Content-Type": "application/json"}


if __name__ == "__main__":
    app.run(port=2808, debug=True)
