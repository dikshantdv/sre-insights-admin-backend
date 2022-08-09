from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_environment_list():
    response = client.get(
        "/data/28008722-f56d-47bd-85c6-e42f03aa7191/environments")
    assert response.status_code == 200
    assert response.json() == {
        "environments": [
            {
                "value": "DCL-PROD-SHORE",
                "label": "DCL-PROD-SHORE",
                "key": "b49d1fcd-5b8d-498c-93d6-90bc1997d569"
            }
        ]
    }


def test_get_environment_list_not_found():
    response = client.get(
        "/data/28008722-f56d-47bd-85c6-e42f03aa7192/environments")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "No environments linked with Job ID 28008722-f56d-47bd-85c6-e42f03aa7192 found"}


def test_get_environment_list_bad_request():
    response = client.get("/data/wrong-uuid/environments")
    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid UUID provided"}


def test_create_task():
    response = client.post("/data/", json={
        "job_environment_id": "5c52de64-53f5-4789-90b6-ad037c5bfa7c"})
    assert response.status_code == 200
    assert list(response.json()["currentTask"][0].keys()) == ["taskid"]


def test_create_task_bad_request():
    response = client.post("/data/", json={
        "job_environment_id": "28008722-f56d-47bd-85c6-e42f03aa7191"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Task creation failed"}


def test_get_lookup():
    response = client.get("/data/")
    assert response.status_code == 200
    assert list(response.json().keys()) == ['jobs', 'tasks']
