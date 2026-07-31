def test_handoff_changes_conversation_state(client):
    response = client.post(
        "/api/v1/chat",
        json={"message": "Quiero hablar con una persona"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["intent"] == "human_handoff"
    assert body["state"] == "waiting_human"
    assert body["tools_used"][0]["name"] == "request_handoff"

    follow_up = client.post(
        "/api/v1/chat",
        json={
            "message": "¿Hay alguien disponible?",
            "conversation_id": body["conversation_id"],
        },
    )
    assert follow_up.status_code == 200
    assert follow_up.json()["provider"] == "workflow"
    assert follow_up.json()["state"] == "waiting_human"


def test_feedback_is_saved(client):
    chat = client.post(
        "/api/v1/chat",
        json={"message": "Hola"},
    )
    conversation_id = chat.json()["conversation_id"]

    response = client.post(
        "/api/v1/feedback",
        json={
            "conversation_id": conversation_id,
            "rating": 5,
            "comment": "Respuesta clara",
        },
    )
    assert response.status_code == 201
    assert response.json()["rating"] == 5


def test_realtime_reports_disabled_without_key(client):
    response = client.get("/api/v1/realtime/config")
    assert response.status_code == 200
    assert response.json()["enabled"] is False
