from ..route_definitions import PUBLIC_ROUTES

def test_public_sites_response_codes(client):
    for route in PUBLIC_ROUTES:
        response = client.get(route)
        assert response.status_code == 200

def test_not_found(client):
    response = client.get("/404")
    assert response.status_code == 404