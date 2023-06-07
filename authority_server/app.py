from config import PASSWORD_HMAC_KEY, COOKIE_KEY
from flask import Flask, request, session
from flask_session import Session
import werkzeug
import hmac
import json
import hashlib
from database import db
from utils import gen_token, gen_encrypt_key, gen_decrypt_key
import datetime
from time import timezone

app = Flask(__name__)

app.config['SECRET_KEY'] = COOKIE_KEY
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(e)
    return "", 400

@app.route('/', methods = ['GET'])
def hello():
    return "Hello world"

@app.route('/api/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hmac.new(bytes(PASSWORD_HMAC_KEY, 'utf-8'), msg=bytes(password, 'utf-8')
                            , digestmod=hashlib.sha256).hexdigest()

    user = db.query("SELECT id, username, role, permission FROM users WHERE username = %s AND password = %s", (username, hashed_password))
    print(user)
    if (len(user) != 1):
        return "Wrong username or password", 401
    session["data"] = user[0]
    return "", 200
    
@app.route('/api/register', methods = ['POST'])
def register():


    if (not request.cookies.get("session") or not session["data"]):
        return "", 401

    if (session["data"]["role"] != "admin"):
        return "", 403

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = db.query("SELECT COUNT(1) AS cnt FROM users WHERE username = %s", (username,))

    hashed_password = hmac.new(bytes(PASSWORD_HMAC_KEY, 'utf-8'), msg=bytes(password, 'utf-8')
                            , digestmod=hashlib.sha256).hexdigest()

    if (user[0]['cnt'] != 0):
        return 409, "Username already exists"
    db.update("INSERT INTO users(username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
    return "", 200

@app.route('/api/parameters', methods = ['GET'])
def parameters():
    if (not request.cookies.get("session") or not session["data"]):
        return "", 401
    
    # TODO: gen param
    dict_param = {}
    dict_param["token"] = gen_token({"permission": session["data"]["permission"], "username": session["data"]["username"], "exp": datetime.datetime.now(tz=datetime.timezone.utc).timestamp() + 3600})
    dict_param["decrypt_key"] = gen_decrypt_key()
    if (session["data"]["permission"]):
        dict_param["encrypt_key"] = gen_encrypt_key()
    
    return dict_param, 200, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(port=2808, debug=True)