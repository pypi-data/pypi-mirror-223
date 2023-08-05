import asyncio
import json
import logging
from datetime import UTC, datetime, timedelta
from enum import Enum, unique
from http import HTTPStatus
from typing import Any, Final

from aiohttp import (
    ClientConnectionError,
    ClientOSError,
    ClientResponse,
    ClientResponseError,
    ClientSession,
    ClientSSLError,
    ServerDisconnectedError,
)

from dabpumps.authentication import Authentication, read_authentication, write_authentication
from dabpumps.installation import Installation
from dabpumps.pump import Pump, PumpState

_LOGGER = logging.getLogger(__name__)

API_BASE_URL: Final[str] = "https://dconnect.dabpumps.com"
API_GET_TOKEN_URL: Final[str] = "/auth/token"
API_GET_INSTALLATION_LIST: Final[str] = "/getInstallationList"
API_GET_INSTALLATION: Final[str] = "/getInstallation/"
API_GET_DUMSTATE: Final[str] = "/dumstate/"

API_EXCEPTION_RETRY_TIME = 0.1
API_RETRY_ATTEMPTS = 10


def _api_headers(access_token: str | None = None) -> dict[str, str]:
    headers = {
        "host": "dconnect.dabpumps.com",
        "accept": "application/json, text/plain, */*",
        "connection": "keep-alive",
        "user-agent": "DabAppFreemium/1 CFNetwork/1406.0.4 Darwin/22.4.0",
        "accept-language": "en-GB,en;q=0.9",
        "accept-encoding": "gzip, deflate, br",
    }

    if access_token:
        headers["authorization"] = f"Bearer {access_token}"

    return headers


def _obscure_payload(payload):
    """Obscure the payload for logging."""
    if payload is None:
        return None
    if "password" in payload:
        payload = payload.copy()
        payload["password"] = "****"  # nosec
    return payload


class DConnect:
    """Class to communicate with the DAB Pumps DConnect API."""

    def __init__(
        self,
        aiohttp_session: ClientSession,
        timeout=10,
        command_timeout=60,
    ) -> None:
        self._timeout = timeout
        self._command_timeout = command_timeout
        self._aiohttp_session = aiohttp_session

    async def authenticate(
        self, email: str, password: str, access_token_cache_file: str | None = None
    ) -> Authentication:
        if access_token_cache_file is not None:
            authentication = await read_authentication(access_token_cache_file)
            if authentication is not None:
                if authentication.is_expired():
                    _LOGGER.error("Access token has expired")
                # If token is to expire within 7 days then print a warning.
                elif (authentication.access_token_expires - datetime.now(UTC)) < timedelta(days=7):
                    _LOGGER.warning(
                        f"Access token is going to expire at {authentication.access_token_expires}. "
                        f"Deleting file {access_token_cache_file} will result "
                        "in a new token being requested next time"
                    )
                    return authentication

        json_dict = await self._get_token(email, password)
        access_token = json_dict["access_token"]
        access_token_expires = datetime.now(UTC) + timedelta(seconds=float(json_dict["expires_in"]))
        authentication = Authentication(access_token, access_token_expires)
        if access_token_cache_file is not None:
            await write_authentication(authentication, access_token_cache_file)

        return authentication

    async def _get_token(self, email: str, password: str):
        return await self._dict_to_api(
            {
                "method": "post",
                "url": API_BASE_URL + API_GET_TOKEN_URL,
                "json": {
                    "email": email,
                    "password": password,
                },
            }
        )

    async def get_installations(self, access_token: str) -> list[Installation]:
        json_dict = await self._dict_to_api(
            {
                "method": "get",
                "url": API_BASE_URL + API_GET_INSTALLATION_LIST,
                "access_token": access_token,
            }
        )
        return [Installation(data) for data in json_dict["rows"]]

    async def get_pumps(self, access_token: str, installation_id: str) -> list[Pump]:
        json_dict = await self._dict_to_api(
            {
                "method": "get",
                "url": API_BASE_URL + API_GET_INSTALLATION + installation_id,
                "access_token": access_token,
            }
        )
        return [Pump(data) for data in json.loads(json_dict["data"])["dumlist"]]

    async def get_pump_state(self, access_token: str, pump_serial: str) -> PumpState:
        json_dict = await self._dict_to_api(
            {
                "method": "get",
                "url": API_BASE_URL + API_GET_DUMSTATE + pump_serial,
                "access_token": access_token,
            }
        )
        timestamp = datetime.fromisoformat(json_dict["statusts"].replace("Z", "+00:00"))
        data = json.loads(json_dict["status"])
        return PumpState(timestamp, data)

    async def _dict_to_api(self, api_dict: dict[str, Any]):
        url = api_dict["url"]
        method = api_dict["method"]
        access_token = api_dict.get("access_token", None)
        del api_dict["url"]
        del api_dict["method"]
        if access_token:
            del api_dict["access_token"]

        payload = api_dict.get("params") or api_dict.get("json")

        if "headers" not in api_dict:
            api_dict["headers"] = _api_headers(access_token=access_token)

        if "timeout" not in api_dict:
            api_dict["timeout"] = self._timeout

        debug_enabled = _LOGGER.isEnabledFor(logging.DEBUG)

        if debug_enabled:
            _LOGGER.debug(
                f"About to call {url} with header={api_dict['headers']} and payload={_obscure_payload(payload)}",
            )

        attempts = 0
        while attempts < API_RETRY_ATTEMPTS:
            attempts += 1
            try:
                response = await self._aiohttp_session.request(method, url, **api_dict)
            except (
                ClientOSError,
                ClientSSLError,
                ServerDisconnectedError,
                ClientConnectionError,
            ) as ex:
                if attempts == API_RETRY_ATTEMPTS:
                    msg = f"Failed to connect to API: {ex}"
                    raise DConnectError(msg) from ex
                await asyncio.sleep(API_EXCEPTION_RETRY_TIME)
                continue
            if debug_enabled:
                _LOGGER.debug(
                    f"Received API response from url: {url!r}, "
                    f"code: {response.status}, "
                    f"headers: {response.headers!r}, "
                    f"content: {await response.read()!r}"
                )
            break

        _raise_response_exceptions(response)

        json_dict = await response.json()
        if json_dict["res"] == "ERROR":
            raise DConnectError(json_dict["msg"], json_dict["code"])

        return json_dict


def _raise_response_exceptions(response: ClientResponse) -> None:
    try:
        response.raise_for_status()
    except ClientResponseError as err:
        if err.status in (HTTPStatus.UNAUTHORIZED, HTTPStatus.FORBIDDEN):
            msg = f"Authentication failed: {err.message}"
            raise DConnectError(msg, str(err.status)) from err
        msg = f"The operation failed with error code {err.status}: {err.message}."
        raise DConnectError(msg, str(err.status)) from err


@unique
class DConnectErrorType(Enum):
    UNKNOWN = "unknown"
    WRONG_CREDENTIAL = "wrongcredential"
    FORBIDDEN = "FORBIDDEN"


class DConnectError(Exception):
    """A DConnect error with a user friendly message."""

    def __init__(self, message: str, code: str | None = None) -> None:
        """Initialize the error."""
        super().__init__(message)
        try:
            self._error_type = DConnectErrorType(code)
        except ValueError:
            self._error_type = DConnectErrorType.UNKNOWN

    @property
    def error_type(self) -> DConnectErrorType:
        return self._error_type
