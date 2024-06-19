import aiohttp

from app.schemas.tg_bot import TelegramBotInfo
from . import exc


class TelegramBot:

    def __init__(self, token: str):
        self._token = token
        self._info: TelegramBotInfo | None = None

    async def get_info(self) -> TelegramBotInfo:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.telegram.org/bot{self._token}/getMe") as resp:
                await self._check_resp_status(resp)
                data = await resp.json()
                info = TelegramBotInfo.model_validate(data["result"])
                self._info = info
                return info

    async def send_message(self, chat_id: int, text: str) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"https://api.telegram.org/bot{self._token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
            ) as resp:
                await self._check_resp_status(resp)
                return True

    async def get_bot_avatar(self) -> bytes:
        if self._info is None:
            await self.get_info()

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.telegram.org/bot{self._token}/getUserProfilePhotos?user_id={self._info.id}"
            ) as files_resp:
                await self._check_resp_status(files_resp)
                data = await files_resp.json()
                file_id = data["result"]["photos"][0][-1]["file_id"]

            async with session.get(
                f"https://api.telegram.org/bot{self._token}/getFile?file_id={file_id}"
            ) as file_resp:
                await self._check_resp_status(file_resp)
                data = await file_resp.json()
                photo_path = data["result"]["file_path"]

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"https://api.telegram.org/file/bot{self._token}/{photo_path}"
            ) as photo_resp:
                await self._check_resp_status(photo_resp)
                photo_data = await photo_resp.read()
                return photo_data

    @staticmethod
    async def _check_resp_status(resp: aiohttp.ClientResponse) -> None:
        if resp.status == 200:
            return None  # no error

        elif resp.status == 400:
            try:
                data = await resp.json()
            except aiohttp.ContentTypeError:
                raise exc.TelegramException("Invalid response")
            else:
                raise exc.TelegramException(data.get("description", "Bad Request"))

        elif resp.status == 401:
            raise exc.TokenInvalid("Invalid token")

        else:
            raise exc.TelegramException(f"Error sending message: {resp.status}")
