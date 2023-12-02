def login(client):
    return client.post("/auth/login/submit", data = {
        "name": "tester",
        "password": ""  # value of the DUMMY_HASH from ..constants
    })
