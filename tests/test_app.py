from fastapi.testclient import TestClient
from urllib.parse import quote

from src.app import app

client = TestClient(app)


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert "Chess Club" in data


def test_signup_and_remove_participant():
    activity = "Art Club"
    email = "tester@example.com"

    # Ensure not present
    r = client.get("/activities")
    assert r.status_code == 200
    assert email not in r.json()[activity]["participants"]

    # Sign up
    path_activity = quote(activity, safe='')
    r = client.post(f"/activities/{path_activity}/signup?email={quote(email, safe='')}")
    assert r.status_code == 200

    # Confirm present
    r = client.get("/activities")
    assert email in r.json()[activity]["participants"]

    # Remove participant
    r = client.delete(f"/activities/{path_activity}/participants?email={quote(email, safe='')}")
    assert r.status_code == 200

    # Confirm removed
    r = client.get("/activities")
    assert email not in r.json()[activity]["participants"]
