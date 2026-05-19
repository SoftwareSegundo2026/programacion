from datetime import timedelta
import unittest
from uuid import uuid4

from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.api.dependencies import get_current_active_user, get_current_user
from app.main import app
from app.auth.service import authenticate_user, create_user_access_token
from app.core.security import create_access_token


class JWTFlowTestCase(unittest.IsolatedAsyncioTestCase):
    async def test_valid_credentials_create_accessible_token(self):
        user = await authenticate_user(None, "admin", "admin123")
        self.assertIsNotNone(user)

        access_token = create_user_access_token(user)
        current_user = await get_current_user(token=access_token)

        self.assertEqual(current_user.username, "admin")
        self.assertEqual(get_current_active_user(current_user=current_user).username, "admin")

    async def test_invalid_credentials_are_rejected(self):
        self.assertIsNone(await authenticate_user(None, "admin", "wrong-password"))

    async def test_expired_token_is_rejected(self):
        expired_token = create_access_token({"sub": "admin"}, expires_delta=timedelta(minutes=-1))

        with self.assertRaises(HTTPException):
            await get_current_user(token=expired_token)

    async def test_inactive_user_is_rejected(self):
        user = await authenticate_user(None, "reader", "reader123")
        self.assertIsNotNone(user)

        access_token = create_user_access_token(user)
        current_user = await get_current_user(token=access_token)

        with self.assertRaises(HTTPException):
            await get_current_active_user(current_user=current_user)

    def test_users_endpoint_lists_and_creates_users(self):
        client = TestClient(app)

        login_response = client.post(
            "/api/v1/auth/token",
            json={"username": "admin", "password": "admin123"},
        )
        self.assertEqual(login_response.status_code, 200)
        access_token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        list_response = client.get("/api/v1/users", headers=headers)
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json()), 2)

        unique_suffix = uuid4().hex[:8]
        create_response = client.post(
            "/api/v1/users",
            headers=headers,
            json={
                "username": f"new_user_{unique_suffix}",
                "email": f"new_user_{unique_suffix}@example.com",
                "full_name": "New User",
                "disabled": False,
                "password": "secret123",
            },
        )
        self.assertEqual(create_response.status_code, 201)
        self.assertEqual(create_response.json()["username"], f"new_user_{unique_suffix}")

        new_login = client.post(
            "/api/v1/auth/token",
            json={
                "username": f"new_user_{unique_suffix}",
                "password": "secret123",
            },
        )
        self.assertEqual(new_login.status_code, 200)


if __name__ == "__main__":
    unittest.main()