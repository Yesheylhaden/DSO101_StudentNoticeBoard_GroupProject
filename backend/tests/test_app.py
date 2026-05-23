from app import app, db, Notice
import os
import pytest
import sys
from pathlib import Path

# Add parent directory to path to import app
sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    # Set test configuration
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://postgres:postgres@localhost:5432/noticeboard_test"
    )

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


class TestHealth:
    """Tests for the health check endpoint."""

    def test_health_check(self, client):
        """Test that the health endpoint returns ok status."""
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'ok'


class TestNotices:
    """Tests for the notices API endpoints."""

    def test_get_announcements_empty(self, client):
        """Test GET /announcements returns empty list when no notices exist."""
        response = client.get('/announcements')
        assert response.status_code == 200
        assert response.json == []

    def test_create_announcement(self, client):
        """Test POST /announcements creates a new notice."""
        notice_data = {
            'title': 'Test Notice',
            'body': 'This is a test notice',
            'category': 'general',
            'author': 'Test Author'
        }
        response = client.post(
            '/announcements',
            json=notice_data,
            content_type='application/json'
        )
        assert response.status_code == 201
        assert response.json['title'] == 'Test Notice'
        assert response.json['author'] == 'Test Author'
        assert 'id' in response.json

    def test_create_announcement_missing_fields(self, client):
        """Test POST /announcements fails when required fields are missing."""
        incomplete_data = {
            'title': 'Test Notice'
            # Missing body and author
        }
        response = client.post(
            '/announcements',
            json=incomplete_data,
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'required' in response.json['error'].lower()

    def test_create_announcement_invalid_category(self, client):
        """Test POST /announcements fails with invalid category."""
        notice_data = {
            'title': 'Test Notice',
            'body': 'This is a test notice',
            'category': 'invalid_category',
            'author': 'Test Author'
        }
        response = client.post(
            '/announcements',
            json=notice_data,
            content_type='application/json'
        )
        assert response.status_code == 400
        assert 'category' in response.json['error'].lower()

    def test_get_announcements_after_creation(self, client):
        """Test GET /announcements returns created notices."""
        notice_data = {
            'title': 'Test Notice 1',
            'body': 'This is test notice 1',
            'category': 'academic',
            'author': 'Author 1'
        }
        # Create a notice
        client.post(
            '/announcements',
            json=notice_data,
            content_type='application/json'
        )

        # Get all notices
        response = client.get('/announcements')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert response.json[0]['title'] == 'Test Notice 1'
        assert response.json[0]['category'] == 'academic'

    def test_get_announcements_returns_latest_first(self, client):
        """Test GET /announcements returns notices in reverse chronological order."""
        # Create first notice
        notice1 = {
            'title': 'First Notice',
            'body': 'First body',
            'category': 'general',
            'author': 'Author 1'
        }
        client.post(
            '/announcements',
            json=notice1,
            content_type='application/json'
        )

        # Create second notice
        notice2 = {
            'title': 'Second Notice',
            'body': 'Second body',
            'category': 'event',
            'author': 'Author 2'
        }
        client.post(
            '/announcements',
            json=notice2,
            content_type='application/json'
        )

        # Get all notices
        response = client.get('/announcements')
        assert response.status_code == 200
        assert len(response.json) == 2
        # Latest notice should be first
        assert response.json[0]['title'] == 'Second Notice'
        assert response.json[1]['title'] == 'First Notice'

    def test_valid_categories(self, client):
        """Test all valid categories are accepted."""
        valid_categories = ['general', 'academic', 'event', 'urgent', 'club']

        for category in valid_categories:
            notice_data = {
                'title': f'Test {category}',
                'body': f'Body for {category}',
                'category': category,
                'author': 'Test Author'
            }
            response = client.post(
                '/announcements',
                json=notice_data,
                content_type='application/json'
            )
            assert response.status_code == 201
            assert response.json['category'] == category
