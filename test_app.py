import pytest
from src.app import app, db, User, Feedback  # <- updated import

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # in-memory test DB
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def register_user(client, email="test@example.com", password="password"):
    return client.post('/register', json={"email": email, "password": password})

def login_user(client, email="test@example.com", password="password"):
    return client.post('/login', json={"email": email, "password": password})

def test_registration(client):
    response = register_user(client)
    assert response.status_code == 201
    assert b"User registered" in response.data

def test_login_success(client):
    register_user(client)
    response = login_user(client)
    assert response.status_code == 200
    assert b"Login successful" in response.data

def test_login_fail(client):
    register_user(client)
    response = client.post('/login', json={"email": "wrong@example.com", "password": "password"})
    assert response.status_code == 401
    assert b"Invalid credentials" in response.data

def test_feedback_submission(client):
    register_user(client)
    login_user(client)
    response = client.post('/feedback', json={"message": "Great tool!"})
    assert response.status_code == 200
    assert b"Feedback submitted" in response.data

def test_feedback_unauthorized(client):
    response = client.post('/feedback', json={"message": "I should not post this."})
    assert response.status_code == 403

def test_admin_feedback_access(client):
    with app.app_context():
        # Create admin user manually
        admin = User(email="admin@example.com", password="hashed", is_admin=True)
        db.session.add(admin)
        db.session.commit()

        # Simulate login by setting session manually
        with client.session_transaction() as sess:
            sess['user_id'] = admin.id

        # Add feedback
        fb = Feedback(message="Test feedback", user_id=admin.id)
        db.session.add(fb)
        db.session.commit()

        # Hit admin endpoint
        response = client.get('/admin/feedbacks')
        assert response.status_code == 200
        assert any("Test feedback" in f["message"] for f in response.get_json())
