import casbin
import mariadb
from auth_middleware import token_required
from charm.toolbox.policytree import PolicyParser
from database import db
from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50 Mb

enforcer = casbin.Enforcer("./abac/model.conf")
parser = PolicyParser()

TABLE_LIST = ["health_records", "person_profiles", "researches", "financials"]


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    print(e)
    return "", 400


@app.route("/", methods=["GET"])
def hello():
    return "Hello world"


@app.route("/search", methods=["POST"])
@token_required
def search(user):
    data = request.json

    uid = data["uid"]
    table = data["table"]
    name = data["name"]
    address = data["address"]
    date_of_birth = data["date_of_birth"]
    if name != "":
        name = "%" + data["name"] + "%"
    if data["address"] != "":
        address = "%" + data["address"] + "%"
    if data["date_of_birth"] != "":
        date_of_birth = "%" + data["date_of_birth"] + "%"
    if table not in TABLE_LIST:
        return "The table does not exist", 400

    params = ()
    if table == "person_profiles":
        sql = f"""
        SELECT
            id, name, file_name, description, last_modified
        FROM
            {table}
        """
        if uid + name + address + sql == "":
            sql += " WHERE 1=0 "
        else:
            sql += " WHERE 1=1 "
        if uid != "":
            sql += " AND id = %d "
            params += (uid,)
        if name != "":
            sql += " AND name LIKE %s "
            params += (name,)
        if address != "":
            sql += " AND address LIKE %s "
            params += (address,)
        if date_of_birth != "":
            sql += " AND date_of_birth LIKE %s "
            params += (date_of_birth,)
    elif table == "researches":
        sql = f"""
        SELECT
            id, name, file_name, description, last_modified
        FROM
            {table}
        """
        if name == "":
            sql += " WHERE 1=0 "
        else:
            sql += " WHERE 1=1 "
        if name != "":
            sql += " AND name LIKE %s "
            params += (name,)
    else:
        sql = f"""
        SELECT
            t1.id, t1.name, t1.file_name, t1.description, t1.last_modified
        FROM
            {table} AS t1
        LEFT JOIN
            person_profiles AS t2 ON t1.uid = t2.id
        """
        if uid + name + address + sql == "":
            sql += " WHERE 1=0 "
        else:
            sql += " WHERE 1=1 "
        if uid != "":
            sql += " AND t1.uid = %d "
            params += (uid,)
        if name != "":
            sql += " AND t1.name LIKE %s "
            params += (name,)
        if address != "":
            sql += " AND t2.address LIKE %s "
            params += (address,)
        if date_of_birth != "":
            sql += " AND t2.date_of_birth LIKE %s "
            params += (date_of_birth,)
    return db.query(sql, params)


@app.route("/pull", methods=["POST"])
@token_required
def pull(user):
    data = request.json

    table = data["table"]
    if table not in TABLE_LIST:
        return "The table does not exist", 400

    policy = db.query(f"SELECT policy FROM {table} WHERE id = %d", (data["id"],))
    if not policy:
        return "Policy not found", 400

    attrs = []
    for attr, vals in user["attributes"].items():
        for val in vals:
            attrs.append(attr + "@" + val)

    tree = parser.parse(policy[0]["policy"])
    if not parser.prune(tree, attrs):
        return "You don't have sufficient permissions", 400

    return db.query(f"SELECT file_name, data FROM {table} WHERE id = %d", (data["id"],))


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
        sql = f"INSERT INTO {table}(uploader_id, name, description, file_name, data, policy, uid) VALUES (?, ?, ?, ?, ?, ?, ?)"
        parameters = (
            user["uid"],
            data["name"],
            data["description"],
            data["file_name"],
            data["data"],
            data["policy"],
            data["uid"],
        )
    elif table == "person_profiles":
        sql = f"INSERT INTO {table}(uploader_id, name, description, file_name, data, policy, address, date_of_birth, id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        parameters = (
            user["uid"],
            data["name"],
            data["description"],
            data["file_name"],
            data["data"],
            data["policy"],
            data["address"],
            data["date_of_birth"],
            data["uid"],
        )
    elif table == "researches":
        sql = f"INSERT INTO {table}(uploader_id, name, description, file_name, data, policy) VALUES (?, ?, ?, ?, ?, ?)"
        parameters = (user["uid"], data["name"], data["description"], data["file_name"], data["data"], data["policy"])
    elif table == "financials":
        sql = f"INSERT INTO {table}(uploader_id, name, description, file_name, data, policy, uid) VALUES (?, ?, ?, ?, ?, ?, ?)"
        parameters = (
            user["uid"],
            data["name"],
            data["description"],
            data["file_name"],
            data["data"],
            data["policy"],
            data["uid"],
        )

    err = db.update(sql, parameters)
    if err:
        if table == "health_records" and isinstance(err, mariadb.IntegrityError):
            return "Please create a person profile first", 500
        return str(err), 500

    return "Upload successful", 200


if __name__ == "__main__":
    app.run("0.0.0.0", 2809)
