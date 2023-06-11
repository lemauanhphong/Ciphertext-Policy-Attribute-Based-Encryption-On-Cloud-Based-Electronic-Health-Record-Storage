import casbin
import mariadb
from auth_middleware import token_required
from database import db
from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
enforcer = casbin.Enforcer("./abac/model.conf")

TABLE_LIST = ["health_records", "person_profiles", "researches", "financials"]


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    print(e)
    return "", 400


@app.route("/", methods=["GET"])
def hello():
    return "Hello world"


@app.route("/pull", methods=["POST"])
@token_required
def pull(user):
    data = request.json

    table = data["table"]
    if table not in TABLE_LIST:
        return "The table does not exist", 400

    # TODO: only test
    sql = f"""
    SELECT t1.*, t2.name, t2.date_of_birth
    FROM {table} AS t1
    LEFT JOIN person_profiles AS t2
    ON t1.uid = t2.uid
    WHERE t1.uid = %d
    OR (t2.address LIKE %s AND t2.date_of_birth = %s)

    """
    return db.query(sql, (data["uid"], data["address"], data["date_of_birth"]))


@app.route("/push", methods=["POST"])
@token_required
def get(user):
    data = request.json

    table = data["table"]
    if table not in TABLE_LIST:
        return "The table does not exist", 400

    act = "push"
    sub = user
    obj = table

    if not enforcer.enforce(sub, obj, act):
        return "You do not have permission to upload files", 403

    if table == "health_records":
        sql = f"INSERT INTO {table}(uploader_id, name, last_modified, description, data, uid) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (user["uid"], data["name"], data["last_modified"], data["description"], data["data"], data["uid"])
    elif table == "person_profiles":
        sql = f"INSERT INTO {table}(uploader_id, name, last_modified, description, data, address, date_of_birth, uid) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (
            user["uid"],
            data["name"],
            data["last_modified"],
            data["description"],
            data["data"],
            data["address"],
            data["date_of_birth"],
            data["uid"],
        )
    elif table == "researches":
        sql = f"INSERT INTO {table}(uploader_id, name, last_modified, description, data) VALUES (?, ?, ?, ?, ?)"
        parameters = (user["uid"], data["name"], data["last_modified"], data["description"], data["data"])
    elif table == "financials":
        sql = f"INSERT INTO {table}(uploader_id, name, last_modified, description, data, uid) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (user["uid"], data["name"], data["last_modified"], data["description"], data["data"], data["uid"])

    err = db.update(sql, parameters)
    if err:
        if table == "health_records" and isinstance(err, mariadb.IntegrityError):
            return "Please create a person profile first", 500
        return "Something went wrong", 500

    return "Upload successful", 200


if __name__ == "__main__":
    app.run("0.0.0.0", 2809)
