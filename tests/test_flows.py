from src import app as app_module


def test_signup_capacity_not_enforced_current_behavior(client):
    # Arrange
    activity_name = "Chess Club"
    email = "capacity-overflow@mergington.edu"
    max_participants = app_module.activities[activity_name]["max_participants"]
    app_module.activities[activity_name]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants)
    ]

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]


def test_activity_name_is_case_sensitive(client):
    # Arrange
    activity_name = "chess club"
    email = "case-test@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_isolation_marker_can_be_added_in_one_test(client):
    # Arrange
    activity_name = "Art Studio"
    email = "isolation-check@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert email in app_module.activities[activity_name]["participants"]


def test_isolation_resets_state_between_tests(client):
    # Arrange
    activity_name = "Art Studio"
    email = "isolation-check@mergington.edu"

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    participants = response.json()[activity_name]["participants"]
    assert email not in participants
