from flask import Flask, request
from database import db
import werkzeug
from auth_middleware import token_required
import os

app = Flask(__name__)

TABLE_LIST = [
    "health_records",
    "person_profiles",
    "research",
    "financials"
]

@app.errorhandler(werkzeug.exceptions.BadRequest)
def handle_bad_request(e):
    print(e)
    return "", 400

@app.route('/', methods = ['GET'])
def hello():
    return "Hello world"

@app.route('/pull', methods = ['POST'])
@token_required
def pull(user):
    table = request.form['table']
    if (table not in TABLE_LIST):
        return "", 400
    
    # TODO: only test
    l = db.query(request.form['sql'])
    return l
        
    
@app.route('/push', methods = ['POST'])
@token_required
def get(user):
    if (user["permission"] != 1):
        return "", 403
    
    table = request.form['table']
    if (table not in TABLE_LIST):
        return "", 400

    # TODO: only test
    db.update(request.form['sql'])
    return "", 200

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    app.run(port=2809, debug=True)