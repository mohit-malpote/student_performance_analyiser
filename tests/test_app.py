from models import db, User


def test_home_route_empty(client):
    """Test home endpoint when database has no users."""
    response = client.get('/')
    assert response.status_code == 200
    assert b"Database Content:" in response.data


def test_home_route_with_users(client, app):
    """Test home endpoint displays user information."""
    with app.app_context():
        u = User(username="prof_jones", password="123", role="hod", name="Prof Jones")
        db.session.add(u)
        db.session.commit()

    response = client.get('/')
    assert response.status_code == 200
    assert b"Prof Jones" in response.data
    assert b"Role: hod" in response.data
    assert b"Username: prof_jones" in response.data
