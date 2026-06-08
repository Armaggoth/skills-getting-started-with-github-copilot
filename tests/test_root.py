"""Tests for the root endpoint."""

import pytest


class TestRootEndpoint:
    """Tests for the GET / endpoint."""

    def test_root_redirect(self, client):
        """Test that root endpoint redirects to /static/index.html."""
        # Arrange
        expected_location = "/static/index.html"
        expected_status_code = 307

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == expected_status_code
        assert response.headers["location"] == expected_location
