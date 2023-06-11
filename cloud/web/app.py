from flask import Flask, request
from database import db
import werkzeug
from auth_middleware import token_required
import os
import casbin

app = Flask(__name__)

enforcer = casbin.Enforcer("./abac/model.conf")

TABLE_LIST = [
    "health_records",
    "person_profiles",
    "researches",
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
    data = request.json
    table = data['table']
    if (table not in TABLE_LIST):
        return "", 400

    # TODO: only test
    sql = """
    SELECT t1.*, t2.name, t2.date_of_birth
    FROM {table} AS t1
    LEFT JOIN person_profiles AS t2
    ON t1.uid = t2.uid
    WHERE t1.uid = %d
    OR (t2.address LIKE %d AND t2.date_of_birth = %s)

    """ % (table, )
    l = db.query(sql, (data['uid'], data['address'], data['date_of_birth']))
    return l
        
@app.route('/push', methods = ['POST'])
@token_required
def get(user):    
    data = request.json

    table = data['table']
    if (table not in TABLE_LIST):
        return "", 400

    act = "push"
    sub = user
    obj = table
    if not enforcer.enforce(sub, obj, act):
        return "", 403
    
    if table == 'health_records':
        sql = f"INSERT INTO {table}(uploader_id, name, date, description, data, uid) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (user['uid'], data['name'], data['date'], data['description'], data['data'], data['uid'])
    elif table =='person_profiles':
        sql = f"INSERT INTO {table}(uploader_id, name, date, description, data, address, date_of_birth, uid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (user['uid'], data['name'], data['date'], data['description'], data['data'], data['address'], data['date_of_birth'], data['uid'])
    elif table == 'researches':
        sql = f"INSERT INTO {table}(uploader_id, name, date, description, data) VALUES (?, ?, ?, ?, ?)"
        parameters = (user['uid'], data['name'], data['date'], data['description'], data['data'])
    elif table == 'financials':
        sql = f"INSERT INTO {table}(uploader_id, name, date, description, data, uid) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (user['uid'], data['name'], data['date'], data['description'], data['data'], data['uid'])

    
    if db.update(sql, parameters):
        return "", 200
    return "", 400

if __name__ == '__main__':
    app.run("0.0.0.0", 2809)