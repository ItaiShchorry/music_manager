"""
US-001: Authentication — register, login, /me

Test cases (input → expected):
  REGISTER_CASES  — POST /auth/register
  LOGIN_CASES     — POST /auth/login
  ME_CASES        — GET /auth/me
"""
import pytest

# ---------------------------------------------------------------------------
# Register cases: (payload, expected_status, check_token_in_response)
# ---------------------------------------------------------------------------
REGISTER_CASES = [
    # Happy path — first user registers OK
    (
        {"email": "artist@example.com", "password": "secret123", "name": "Amit"},
        201,
        True,
    ),
    # Missing required field
    (
        {"email": "artist@example.com", "name": "Amit"},  # no password
        422,
        False,
    ),
    # Invalid email format
    (
        {"email": "not-an-email", "password": "secret123", "name": "Amit"},
        422,
        False,
    ),
]

# ---------------------------------------------------------------------------
# Login cases: (email, password, expected_status, check_token)
# ---------------------------------------------------------------------------
LOGIN_CASES = [
    # Happy path
    ("test@example.com", "password123", 200, True),
    # Wrong password
    ("test@example.com", "wrongpassword", 401, False),
    # Non-existent user
    ("nobody@example.com", "password123", 401, False),
]

# ---------------------------------------------------------------------------
# Single-user lock: second registration must be rejected
# ---------------------------------------------------------------------------


class TestRegister:
    def test_happy_path(self, client):
        resp = client.post(
            "/api/v1/auth/register",
            json={"email": "artist@example.com", "password": "secret123", "name": "Amit"},
        )
        assert resp.status_code == 201
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_missing_password_returns_422(self, client):
        resp = client.post(
            "/api/v1/auth/register",
            json={"email": "artist@example.com", "name": "Amit"},
        )
        assert resp.status_code == 422

    def test_invalid_email_returns_422(self, client):
        resp = client.post(
            "/api/v1/auth/register",
            json={"email": "not-an-email", "password": "secret123", "name": "Amit"},
        )
        assert resp.status_code == 422

    def test_single_user_lock_blocks_second_registration(self, client, sample_user):
        # sample_user fixture already created a user in the DB
        resp = client.post(
            "/api/v1/auth/register",
            json={"email": "second@example.com", "password": "pass123", "name": "Second"},
        )
        assert resp.status_code == 403
        assert "single-user" in resp.json()["detail"].lower()


class TestLogin:
    @pytest.mark.parametrize("email,password,expected_status,has_token", LOGIN_CASES)
    def test_login(self, client, sample_user, email, password, expected_status, has_token):
        resp = client.post(
            "/api/v1/auth/login",
            data={"username": email, "password": password},
        )
        assert resp.status_code == expected_status
        if has_token:
            assert "access_token" in resp.json()


class TestMe:
    def test_me_authenticated(self, client, sample_user, auth_headers):
        resp = client.get("/api/v1/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == sample_user.email
        assert data["name"] == sample_user.name
        assert "id" in data

    def test_me_unauthenticated_returns_401(self, client):
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    def test_me_invalid_token_returns_401(self, client):
        resp = client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid.token.here"})
        assert resp.status_code == 401
