def test_live(client):
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_ready(client):
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["ai_provider"] == "demo"


def test_frontend_is_served(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "FerreBot Conversational AI" in response.text
