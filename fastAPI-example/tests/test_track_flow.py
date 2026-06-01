import unittest
from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


class TrackFlowTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        login_response = cls.client.post(
            "/api/v1/auth/token",
            json={"username": "admin", "password": "admin123"},
        )
        if login_response.status_code != 200:
            raise AssertionError("Unable to authenticate test user for Track flow")
        access_token = login_response.json()["access_token"]
        cls.headers = {"Authorization": f"Bearer {access_token}"}

    def test_tracks_endpoint_crud(self):
        list_response = self.client.get(
            "/api/v1/tracks",
            headers=self.headers,
            params={"skip": 0, "limit": 1},
        )
        self.assertEqual(list_response.status_code, 200)
        self.assertGreaterEqual(len(list_response.json()), 1)

        first_track = list_response.json()[0]
        self.assertIn("AlbumTitle", first_track)
        self.assertIn("GenreName", first_track)
        self.assertIn("MediaTypeName", first_track)

        track_id = None
        unique_suffix = uuid4().hex[:8]

        try:
            create_response = self.client.post(
                "/api/v1/tracks",
                headers=self.headers,
                json={
                    "Name": f"Track de prueba {unique_suffix}",
                    "AlbumId": 1,
                    "MediaTypeId": 1,
                    "GenreId": 1,
                    "Composer": "Copilot Test",
                    "Milliseconds": 123456,
                    "Bytes": 654321,
                    "UnitPrice": 0.99,
                },
            )
            self.assertEqual(create_response.status_code, 201)

            created = create_response.json()
            track_id = created["TrackId"]
            self.assertEqual(created["Name"], f"Track de prueba {unique_suffix}")
            self.assertEqual(created["MediaTypeName"], "MPEG audio file")

            read_response = self.client.get(
                f"/api/v1/tracks/{track_id}",
                headers=self.headers,
            )
            self.assertEqual(read_response.status_code, 200)
            self.assertEqual(read_response.json()["TrackId"], track_id)

            update_response = self.client.patch(
                f"/api/v1/tracks/{track_id}",
                headers=self.headers,
                json={"Name": f"Track de prueba {unique_suffix} actualizado"},
            )
            self.assertEqual(update_response.status_code, 200)
            self.assertEqual(
                update_response.json()["Name"],
                f"Track de prueba {unique_suffix} actualizado",
            )

            delete_response = self.client.delete(
                f"/api/v1/tracks/{track_id}",
                headers=self.headers,
            )
            self.assertEqual(delete_response.status_code, 204)
            track_id = None
        finally:
            if track_id is not None:
                self.client.delete(f"/api/v1/tracks/{track_id}", headers=self.headers)


if __name__ == "__main__":
    unittest.main()