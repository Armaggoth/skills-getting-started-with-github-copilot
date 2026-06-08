"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest
from urllib.parse import quote_plus
from src.app import activities


class TestSignupEndpoint:
    """Tests for the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client):
        """Test successful signup for an activity."""
        # Arrange
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        expected_status = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )

        # Assert
        assert response.status_code == expected_status
        data = response.json()
        assert f"Signed up {new_email} for {activity_name}" in data["message"]
        assert new_email in activities[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup with non-existent activity."""
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        expected_status = 404
        expected_detail = "Activity not found"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={email}"
        )

        # Assert
        assert response.status_code == expected_status
        data = response.json()
        assert expected_detail in data["detail"]

    def test_signup_already_registered(self, client):
        """Test duplicate signup for same activity."""
        # Arrange
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        expected_status = 400

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={existing_email}"
        )

        # Assert
        assert response.status_code == expected_status
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_adds_to_participants_list(self, client):
        """Test that signup correctly adds to the participants list."""
        # Arrange
        activity_name = "Programming Class"
        new_email = "newstudent@mergington.edu"
        initial_count = len(activities[activity_name]["participants"])

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={new_email}"
        )

        # Assert
        assert response.status_code == 200
        assert len(activities[activity_name]["participants"]) == initial_count + 1

    def test_signup_with_special_characters_in_email(self, client):
        """Test signup with email containing special characters."""
        # Arrange
        activity_name = "Chess Club"
        email = "john+test@mergington.edu"
        encoded_email = quote_plus(email)
        expected_status = 200

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup?email={encoded_email}"
        )

        # Assert
        assert response.status_code == expected_status
        assert email in activities[activity_name]["participants"]

    def test_signup_multiple_students_same_activity(self, client):
        """Test multiple different students can sign up for the same activity."""
        # Arrange
        activity_name = "Chess Club"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        expected_status = 200

        # Act
        response1 = client.post(f"/activities/{activity_name}/signup?email={email1}")
        response2 = client.post(f"/activities/{activity_name}/signup?email={email2}")

        # Assert
        assert response1.status_code == expected_status
        assert response2.status_code == expected_status
        assert email1 in activities[activity_name]["participants"]
        assert email2 in activities[activity_name]["participants"]
