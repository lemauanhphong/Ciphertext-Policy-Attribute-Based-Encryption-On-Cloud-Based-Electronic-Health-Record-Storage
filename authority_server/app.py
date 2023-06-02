from flask import Flask, request, Response, session
from flask_session import Session
import hmac
import hashlib
from database import db

app = Flask(__name__)

app.config['SECRET_KEY'] = "aaa"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

SECRET = "secret_one"

@app.route('/', methods = ['GET'])
def hello():
    return "Hello world"

@app.route('/api/login', methods = ['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        hashed_password = hmac.new(bytes(SECRET, 'utf-8'), msg=bytes(password, 'utf-8')
                                , digestmod=hashlib.sha256).hexdigest()
        user = db.query("SELECT username FROM users WHERE username = %s AND password = %s", (username, hashed_password))

        if (len(user) != 1):
            resp = Response(response="Wrong username or password", status=401)
        else:
            session["data"]={"username": user[0][0], "role": user[0][1]}
            resp = Response(status=200)
        return resp
    except Exception as e:
        print(e)
        return Response(status=400)
    
@app.route('/api/register', methods = ['POST'])
def login():
    try:
        username = request.form['username']
        password = request.form['password']
        hashed_password = hmac.new(bytes(SECRET, 'utf-8'), msg=bytes(password, 'utf-8')
                                , digestmod=hashlib.sha256).hexdigest()
        user = db.query("SELECT COUNT(1) FROM users WHERE username = %s", (username,))

        if (user[0] != 0):
            resp = Response(response="Username already exists", status=409)
        else:
            db.update("INSERT INTO users WHERE username = %s AND password = %s", (username, password,))
            resp = Response(status=200)
        return resp
    except Exception as e:
        print(e)
        return Response(status=400)

if __name__ == '__main__':
    app.run(port=2808, debug=True)