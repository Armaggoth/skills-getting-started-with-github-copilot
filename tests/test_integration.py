"""Integration tests for multiple endpoints."""

import pytest
from src.app import activities


class TestEndpointIntegration:
    """Integration tests combining multiple endpoints."""

    def test_signup_then_remove_participant(self, client):
        """Test signing up and then removing a participant."""
        # Arrange
        email = "tempstudent@mergington.edu"
        activity_name = "Chess Club"

        # Act - Sign up
        response1 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )
        assert response1.status_code == 200

        # Assert signup worked
        assert email in activities[activity_name]["participants"]

        # Act - Remove
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert removal worked
        assert response2.status_code == 200
        assert email not in activities[activity_name]["participants"]

    def test_multiple_signups_different_activities(self, client):
        """Test signing up for multiple different activities."""
        # Arrange
        email = "multistudent@mergington.edu"
        activities_to_join = ["Chess Club", "Programming Class", "Gym Class"]

        # Act
        responses = [
            client.post(f"/activities/{activity}/signup?email={email}")
            for activity in activities_to_join
        ]

        # Assert
        for response in responses:
            assert response.status_code == 200
        for activity in activities_to_join:
            assert email in activities[activity]["participants"]

    def test_get_activities_reflects_changes(self, client):
        """Test that GET /activities reflects signup and removal changes."""
        # Arrange
        email = "changestudent@mergington.edu"
        activity_name = "Chess Club"

        # Act - Sign up and verify in GET
        client.post(f"/activities/{activity_name}/signup?email={email}")
        response1 = client.get("/activities")
        data1 = response1.json()

        # Assert signup is reflected
        assert email in data1[activity_name]["participants"]

        # Act - Remove and verify in GET
        client.delete(f"/activities/{activity_name}/participants/{email}")
        response2 = client.get("/activities")
        data2 = response2.json()

        # Assert removal is reflected
        assert email not in data2[activity_name]["participants"]

    def test_signup_conflict_then_remove_then_signup_again(self, client):
        """Test trying to signup twice, then removing, then signing up again."""
        # Arrange
        email = "testconflict@mergington.edu"
        activity_name = "Chess Club"
        expected_conflict_status = 400
        expected_success_status = 200

        # Act - First signup succeeds
        response1 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert first signup
        assert response1.status_code == expected_success_status

        # Act - Second signup fails (already registered)
        response2 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert second signup fails
        assert response2.status_code == expected_conflict_status

        # Act - Remove
        response3 = client.delete(
            f"/activities/{activity_name}/participants/{email}"
        )

        # Assert removal works
        assert response3.status_code == expected_success_status

        # Act - Signup again succeeds
        response4 = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert signup again succeeds
        assert response4.status_code == expected_success_status
        assert email in activities[activity_name]["participants"]

    def test_full_activity_lifecycle(self, client):
        """Test full lifecycle: add multiple students, view, remove one, view again."""
        # Arrange
        email1 = "lifecycle1@mergington.edu"
        email2 = "lifecycle2@mergington.edu"
        activity_name = "Chess Club"

        # Act - Add two students
        client.post(f"/activities/{activity_name}/signup?email={email1}")
        client.post(f"/activities/{activity_name}/signup?email={email2}")

        # Assert - Get and verify both are there
        response1 = client.get("/activities")
        data1 = response1.json()
        count_before = len(data1[activity_name]["participants"])

        # Act - Remove one
        client.delete(f"/activities/{activity_name}/participants/{email1}")

        # Assert - Get and verify only one remains
        response2 = client.get("/activities")
        data2 = response2.json()
        count_after = len(data2[activity_name]["participants"])

        assert count_after == count_before - 1
        assert email1 not in data2[activity_name]["participants"]
        assert email2 in data2[activity_name]["participants"]
