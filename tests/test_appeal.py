def test_no_input(client):
    response = client.post("/support/appeal", data={})
    assert response.status_code == 400

def test_wrong_input(client):
    response = client.post("/support/appeal", data= {
        "player": "_$)%/FEUBIUFB"
    })
    assert response.status_code == 400

def test_not_banned(client):
    response = client.post("/support/appeal", data= {
        "player": "NONEXISTENT"
    })
    assert response.status_code == 400