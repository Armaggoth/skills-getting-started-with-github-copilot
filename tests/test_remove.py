"""Tests for the DELETE /activities/{activity_name}/participants/{participant_email} endpoint."""

import pytest
from src.app import activities


class TestRemoveParticipantEndpoint:
    """Tests for the DELETE /activities/{activity_name}/participants/{participant_email} endpoint."""

    def test_remove_participant_success(self, client):
        """Test successful removal of a participant."""
        # Arrange
        activity_name = "Chess Club"
        participant_email = "michael@mergington.edu"
        expected_status = 200

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        # Assert
        assert response.status_code == expected_status
        data = response.json()
        assert f"Removed {participant_email} from {activity_name}" in data["message"]
        assert participant_email not in activities[activity_name]["participants"]

    def test_remove_participant_activity_not_found(self, client):
        """Test removal from non-existent activity."""
        # Arrange
        activity_name = "Nonexistent Club"
        participant_email = "student@mergington.edu"
        expected_status = 404
        expected_detail = "Activity not found"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        # Assert
        assert response.status_code == expected_status
        data = response.json()
        assert expected_detail in data["detail"]

    def test_remove_participant_not_found(self, client):
        """Test removal of participant not in activity."""
        # Arrange
        activity_name = "Chess Club"
        participant_email = "notfound@mergington.edu"
        expected_status = 404
        expected_detail = "Participant not found"

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        # Assert
        assert response.status_code == expected_status
        data = response.json()
        assert expected_detail in data["detail"]

    def test_remove_participant_reduces_list(self, client):
        """Test that removing a participant reduces the list size."""
        # Arrange
        activity_name = "Gym Class"
        participant_email = "john@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        # Assert
        assert response.status_code == 200
        assert len(activities[activity_name]["participants"]) == initial_count - 1

    def test_remove_participant_twice(self, client):
        """Test that removing the same participant twice fails."""
        # Arrange
        activity_name = "Chess Club"
        participant_email = "michael@mergington.edu"

        # Act
        response1 = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )
        response2 = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        # Assert
        assert response1.status_code == 200
        assert response2.status_code == 404

    def test_remove_participant_does_not_affect_other_activities(self, client):
        """Test that removing from one activity doesn't affect others."""
        # Arrange
        email = "multistudent@mergington.edu"
        activity1 = "Chess Club"
        activity2 = "Programming Class"

        client.post(f"/activities/{activity1}/signup?email={email}")
        client.post(f"/activities/{activity2}/signup?email={email}")

        # Act
        response = client.delete(
            f"/activities/{activity1}/participants/{email}"
        )

        # Assert
        assert response.status_code == 200
        assert email not in activities[activity1]["participants"]
        assert email in activities[activity2]["participants"]
