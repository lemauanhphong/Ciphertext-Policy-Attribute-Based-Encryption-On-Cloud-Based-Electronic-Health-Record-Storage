from requests import Session
import json

AS_SERVER = "http://localhost:2808/"
CLOUD_SERVER = "http://localhost:2809/"
account = {"username": "admin", "password": "password"}

s = Session()
r = s.post(AS_SERVER + "api/login", json=account)
print(r.text)
r = s.get(AS_SERVER + "api/parameters")
print(json.dumps(r.json(), indent=4))

token = r.json()["token"]
seckey = r.json()["secret_key"]
pubkey = r.json()["public_key"]

# ------------------------------

# with open("encrypted_files/ui_files_watchdog.py.enc", "r") as f:
#    content = f.read()
content = "super encryption provjp123"

data = [
    {
        "table": "person_profiles",
        "uid": 25519,
        "name": "Tony Stark",
        "address": "Hai Phong",
        "date_of_birth": "1997-01-01",
        "data": content,
        "date": "2023-01-01",
        "description": "bro",
    },
    {
        "table": "health_records",
        "uid": 25519,
        "name": "Tony Stark has a heart attack",
        "date": "2023-01-01",
        "data": "uh uh no... ded..",
        "description": "lmao",
    },
    {
        "table": "researches",
        "name": "research about secret power of steve rogers",
        "date": "2023-01-01",
        "description": "oxjt",
        "data": "this is data bro",
    },
    {
        "table": "financials",
        "uid": "1337",
        "name": "chi tieu tai chinh cua lien hop quoc",
        "date": "2021-10-10",
        "description": "tai lieu nay da duoc bao cao len lien hop quoc",
        "data": "-10000$",
    },
]
search_data = [{"table": "health_records", "uid": 25519, "address": "", "date_of_birth": ""}]


s.headers["Authorization"] = "Bearer " + token

for d in data:
    r = s.post(CLOUD_SERVER + "push", json=d)
    print(r.text)


for d in search_data:
    r = s.post(CLOUD_SERVER + "pull", json=d)
    print(json.dumps(r.json(), indent=4))
