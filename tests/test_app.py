"""Tests for FastAPI Mergington High School API"""

from fastapi.testclient import TestClient


def test_get_activities(client: TestClient):
    # Arrange: client fixture

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "programming" not in data  # ensure case sensitive for key


def test_signup_for_activity_success(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "student1@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Signed up" in body["message"]

    followup = client.get("/activities").json()
    assert email in followup[activity_name]["participants"]


def test_signup_for_activity_not_found(client: TestClient):
    # Arrange
    activity_name = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": "student@x.com"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_delete_unregister_success(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]


def test_delete_unregister_not_signed_up(client: TestClient):
    # Arrange
    activity_name = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_delete_unregister_activity_not_found(client: TestClient):
    # Arrange
    activity_name = "Club Missing"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": "student@x.com"})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
