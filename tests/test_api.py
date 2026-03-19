from fastapi.testclient import TestClient
from app.main import app

#REFERENCE: Code adpated from ChatGPT 
# https://chatgpt.com/share/69bbe8f9-a48c-8002-ae14-84833f2152b6


client = TestClient(app)


def test_create_run():
    """Test creating a valid run"""

    response = client.post("/runs", json={
        "title": "Test Run",
        "date": "2026-03-14",
        "distance_km": 5,
        "duration_minutes": 25,
        "run_type": "easy",
        "notes": "pytest test",
        "gender": "Women",
        "age": 20
    })

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Test Run"
    assert data["distance_km"] == 5
    assert data["gender"] == "Women"
    assert "id" in data


def test_get_runs():
    """Test retrieving runs"""

    response = client.get("/runs")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_missing_fields():
    """Test validation error when fields are missing"""

    response = client.post("/runs", json={
        "title": "Bad Run"
    })

    assert response.status_code == 422


def test_get_nonexistent_run():
    """Test requesting a run that does not exist"""

    response = client.get("/runs/999999")

    assert response.status_code == 404


def test_delete_run():
    """Test deleting a run"""

    # First create one
    create = client.post("/runs", json={
        "title": "Delete Test",
        "date": "2026-03-14",
        "distance_km": 5,
        "duration_minutes": 30,
        "run_type": "easy",
        "notes": "delete me",
        "gender": "Women",
        "age": 22
    })

    run_id = create.json()["id"]

    # Now delete it
    delete = client.delete(f"/runs/{run_id}")

    assert delete.status_code == 200
    assert delete.json()["message"] == "Run deleted successfully"


def test_compare_invalid_run():
    """Test compare endpoint with invalid id"""

    response = client.get("/compare/99999")

    assert response.status_code == 404