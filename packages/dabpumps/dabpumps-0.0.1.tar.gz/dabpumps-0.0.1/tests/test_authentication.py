from datetime import UTC, datetime, timedelta

import aiounittest

from dabpumps.authentication import (
    Authentication,
    authentication_from_json,
    authentication_to_json,
)


class TestAuthentication(aiounittest.AsyncTestCase):
    def setUp(self):
        """Setup things to be run when tests are started."""

    def test_authentication_to_from_json(self):
        first = Authentication(
            "access-token",
            datetime.now(UTC) + timedelta(days=1),
        )
        s = authentication_to_json(first)
        second = authentication_from_json(s)
        self.assertEqual(first.access_token, second.access_token)
        self.assertEqual(first.access_token_expires, second.access_token_expires)
        self.assertEqual(first.is_expired(), second.is_expired())
