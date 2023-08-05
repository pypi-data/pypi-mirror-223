import json
import logging
import os
from datetime import UTC, datetime

import aiofiles

_LOGGER = logging.getLogger(__name__)


class Authentication:
    def __init__(
        self,
        access_token: str,
        access_token_expires: datetime,
    ):
        self._access_token = access_token
        self._access_token_expires = access_token_expires

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def access_token_expires(self) -> datetime:
        return self._access_token_expires

    def is_expired(self) -> bool:
        return self._access_token_expires < datetime.now(UTC)


def authentication_from_json(content: str) -> Authentication:
    if content is None:
        return None
    data = json.loads(content)
    access_token = data["access_token"]
    access_token_expires = datetime.fromisoformat(data["access_token_expires"])
    return Authentication(access_token, access_token_expires)


def authentication_to_json(authentication: Authentication) -> str:
    if authentication is None:
        return json.dumps({})

    return json.dumps(
        {
            "access_token": authentication.access_token,
            "access_token_expires": authentication.access_token_expires.isoformat(),
        }
    )


async def read_authentication(file_name: str) -> Authentication | None:
    if file_name is not None and os.path.exists(file_name):
        async with aiofiles.open(file_name, "r") as file:
            try:
                return authentication_from_json(await file.read())
            except json.decoder.JSONDecodeError as error:
                _LOGGER.error(
                    f"Unable to read authentication file ({file_name}): {error}",
                )
    return None


async def write_authentication(authentication: Authentication, file_name: str) -> None:
    if authentication is not None and file_name is not None:
        async with aiofiles.open(file_name, "w") as file:
            await file.write(authentication_to_json(authentication))
