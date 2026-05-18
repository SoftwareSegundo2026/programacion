from datetime import timedelta
import unittest

from fastapi import HTTPException

from app.api.dependencies import get_current_active_user, get_current_user
from app.auth.service import authenticate_user, create_user_access_token
from app.core.security import create_access_token


class JWTFlowTestCase(unittest.TestCase):
    def test_valid_credentials_create_accessible_token(self):
        user = authenticate_user("admin", "admin123")
        self.assertIsNotNone(user)

        access_token = create_user_access_token(user)
        current_user = get_current_user(token=access_token)

        self.assertEqual(current_user.username, "admin")
        self.assertEqual(get_current_active_user(current_user=current_user).username, "admin")

    def test_invalid_credentials_are_rejected(self):
        self.assertIsNone(authenticate_user("admin", "wrong-password"))

    def test_expired_token_is_rejected(self):
        expired_token = create_access_token({"sub": "admin"}, expires_delta=timedelta(minutes=-1))

        with self.assertRaises(HTTPException):
            get_current_user(token=expired_token)

    def test_inactive_user_is_rejected(self):
        user = authenticate_user("reader", "reader123")
        self.assertIsNotNone(user)

        access_token = create_user_access_token(user)
        current_user = get_current_user(token=access_token)

        with self.assertRaises(HTTPException):
            get_current_active_user(current_user=current_user)


if __name__ == "__main__":
    unittest.main()