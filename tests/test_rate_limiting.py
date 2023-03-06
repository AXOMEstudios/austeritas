from ..constants import MESSAGE_LIMIT, MAX_CONTENT_SIZE

def test_too_large_request_entity(client):
    response = client.post("/support/message", data = {
        "data": "a" * (MAX_CONTENT_SIZE + 1)
    })
    assert response.status_code == 413

def test_message_rate_limits(client):
    for _ in range(int(MESSAGE_LIMIT.split("/")[0]) + 5):
        response = client.get("/support/message")
        print(response.status_code)

    assert response.status_code == 429

def test_message_conforming_rate_limits(client):
    for _ in range(int(MESSAGE_LIMIT.split("/")[0]) - 1):
        response = client.get("/support/message")
        print(response.status_code)

    assert response.status_code == 200
