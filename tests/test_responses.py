from ..route_definitions import PUBLIC_ROUTES

def test_public_sites_response_codes(client):
    for route in PUBLIC_ROUTES:
        response = client.get(route)
        assert response.status_code == 200