import aiohttp

from app.schemas.auth import TokenSchema, LoginSchema, UserSchema
from app.settings import settings


class _EcstasyApi:

    async def get_jwt(self, user_data: LoginSchema) -> TokenSchema:
        async with aiohttp.ClientSession(base_url=settings.ecstasy_url) as session:
            async with session.post("/api/token", data=user_data.model_dump()) as response:
                data = await self._get_json_data(response)
                return TokenSchema(**data)

    @staticmethod
    async def verify_jwt(token: str) -> bool:
        async with aiohttp.ClientSession(base_url=settings.ecstasy_url) as session:
            async with session.post("/api/token/verify", data={"token": token}) as response:
                return response.status == 200

    async def refresh_jwt(self, refresh_token: str) -> TokenSchema:
        async with aiohttp.ClientSession(base_url=settings.ecstasy_url) as session:
            async with session.post("/api/token/refresh", data={"refresh": refresh_token}) as response:
                data = await self._get_json_data(response)
                return TokenSchema(**data)

    async def get_myself(self, token: str) -> UserSchema:
        async with aiohttp.ClientSession(base_url=settings.ecstasy_url) as session:
            async with session.get(
                "/api/v1/accounts/myself", headers={"Authorization": f"Bearer {token}"}
            ) as response:
                data = await self._get_json_data(response)
                return UserSchema(**data)

    async def get_myself_permissions(self, token: str) -> list[str]:
        async with aiohttp.ClientSession(base_url=settings.ecstasy_url) as session:
            async with session.get(
                "/api/v1/accounts/myself/permissions", headers={"Authorization": f"Bearer {token}"}
            ) as response:
                data = await self._get_json_data(response)
                return data.get("permissions", [])

    async def _get_json_data(self, response: aiohttp.ClientResponse) -> dict:
        await self._raise_for_status(response)
        try:
            return await response.json()
        except aiohttp.ContentTypeError:
            return {}

    @staticmethod
    async def _raise_for_status(response: aiohttp.ClientResponse) -> None:
        """
        Raises an exception if the response status code is not 200.
        :return: None
        :raises class:aiohttp.ClientResponseError:
        """
        if response.status == 200:
            return

        data = await response.json()
        if "Given token not valid for any token type" in data.get("detail", ""):
            response.status = 401
            data["detail"] = "Token is invalid"

        raise aiohttp.ClientResponseError(
            status=response.status,
            message=data.get("detail", response.reason),
            history=response.history,
            request_info=response.request_info,
        )


ecstasy_api: _EcstasyApi = _EcstasyApi()
