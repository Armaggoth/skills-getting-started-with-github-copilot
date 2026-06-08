"""Tests for the GET /activities endpoint."""

import pytest


class TestGetActivitiesEndpoint:
    """Tests for the GET /activities endpoint."""

    def test_get_activities_success(self, client):
        """Test retrieving all activities."""
        # Arrange
        expected_activities = ["Chess Club", "Programming Class", "Gym Class"]
        expected_chess_club_max = 12
        expected_chess_club_participants = 2

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        for activity in expected_activities:
            assert activity in data
        assert data["Chess Club"]["max_participants"] == expected_chess_club_max
        assert len(data["Chess Club"]["participants"]) == expected_chess_club_participants

    def test_get_activities_returns_dict(self, client):
        """Test that activities endpoint returns a dict, not a list."""
        # Arrange
        expected_type = dict

        # Act
        response = client.get("/activities")
        data = response.json()

        # Assert
        assert response.status_code == 200
        assert isinstance(data, expected_type)

    def test_get_activities_includes_full_details(self, client):
        """Test that each activity has all required fields."""
        # Arrange
        required_fields = ["description", "schedule", "max_participants", "participants"]

        # Act
        response = client.get("/activities")
        data = response.json()
        activity = data["Chess Club"]

        # Assert
        for field in required_fields:
            assert field in activity
        assert isinstance(activity["participants"], list)
