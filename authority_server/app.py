from flask import Flask, request, Response, session, redirect
from flask_session import Session
import werkzeug
import hmac
import json
import hashlib
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = "aaa" # for cookie
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SECRET = "secret_one" # for password hashing

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(e)
    return Response(status=400)

@app.route('/', methods = ['GET'])
def hello():
    return "Hello world"

@app.route('/api/login', methods = ['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    hashed_password = hmac.new(bytes(SECRET, 'utf-8'), msg=bytes(password, 'utf-8')
                            , digestmod=hashlib.sha256).hexdigest()
    user = db.query("SELECT username, role, permission FROM users WHERE username = %s AND password = %s", (username, hashed_password))

    if (len(user) != 1):
        resp = Response(response="Wrong username or password", status=401)
    else:
        session["data"] = {"username": user[0][0], "role": user[0][1], "permission": user[0][2]}
        resp = Response(status=200)
    return resp
    
@app.route('/api/register', methods = ['POST'])
def register():
    if (not session["data"]):
        return Response(status=401)

    if (session["data"]["role"] != "admin"):
        return Response(status=403)

    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    user = db.query("SELECT COUNT(1) FROM users WHERE username = %s", (username,))

    hashed_password = hmac.new(bytes(SECRET, 'utf-8'), msg=bytes(password, 'utf-8')
                            , digestmod=hashlib.sha256).hexdigest()

    if (user[0][0] != 0):
        resp = Response(response="Username already exists", status=409)
    else:
        db.update("INSERT INTO users(username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, role))
        resp = Response(status=200)
    return resp

@app.route('/api/parameters', methods = ['GET'])
def parameters():
    if (not session["data"]):
        return Response(status=401)
    
    # TODO: gen param
    dict_param = {}
    dict_param["token"] = ""
    dict_param["decrypt_key"] = ""
    if (session["data"]["permission"]):
        dict_param["encrypt_key"] = ""
    
    return Response(200, response=json.dumps(dict_param), mimetype="application/json")

if __name__ == '__main__':
    app.run(port=2808, debug=True)