from app.schemas.auth import UserSchema
from app.schemas.notifications import (
    ChatSchema,
    TelegramBotNotificationSchema,
    CreateTelegramBotNotificationSchema,
    UpdateTelegramBotNotificationSchema,
    UpdateChatSchema,
)
from app.services.auth import get_current_user
from app.services.notifications.config import NotificationsConfig
from app.services.notifications.exc import TelegramException, TokenInvalid
from app.services.notifications.telegram import TelegramBot
from fastapi import APIRouter, HTTPException, Depends, Response

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notifications_config(_: UserSchema = Depends(get_current_user)) -> NotificationsConfig:
    return NotificationsConfig()


@router.get("/telegram", response_model=list[TelegramBotNotificationSchema])
async def get_telegram_notifications(config: NotificationsConfig = Depends(get_notifications_config)):
    notifications = config.get_telegram_notifications()
    return notifications


@router.post("/telegram", status_code=201)
async def create_telegram_notification(
        data: CreateTelegramBotNotificationSchema, config: NotificationsConfig = Depends(get_notifications_config)
):
    config.add_telegram_notification(
        name=data.name,
        token=data.token,
        description=data.description,
    )


@router.patch("/telegram/{notification_name}", status_code=200)
async def update_telegram_notification(
        notification_name: str,
        data: UpdateTelegramBotNotificationSchema,
        config: NotificationsConfig = Depends(get_notifications_config),
):
    try:
        config.update_telegram_notification(
            notification_name,
            token=data.token,
            new_name=data.name,
            description=data.description,
        )
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.delete("/telegram/{notification_name}", status_code=204)
async def delete_telegram_notification(
        notification_name: str, config: NotificationsConfig = Depends(get_notifications_config)
):
    try:
        config.delete_telegram_notification(notification_name)
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.get(
    "/telegram/{notification_name}/avatar",
    responses={200: {"content": {"image/jpg": {}}}},
    response_class=Response,
)
async def get_telegram_notification_avatar(
        notification_name: str, config: NotificationsConfig = Depends(get_notifications_config)
):
    try:
        tg_bot = TelegramBot(config.get_telegram_notification(notification_name).token)
        headers = {
            "Cache-Control": "public, max-age=300",
        }
        return Response(await tg_bot.get_bot_avatar(), media_type="image/jpg", headers=headers)
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    except TokenInvalid:
        raise HTTPException(
            status_code=401, detail=f"Неверный токен бота для телеграм оповещения '{notification_name}'"
        )
    except TelegramException as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при получении аватарки бота телеграм оповещения '{notification_name}': {exc.detail}",
        )


# ================================== CHATS ===================================


@router.get("/telegram/{notification_name}/chats", response_model=list[ChatSchema])
async def get_telegram_notification_chats(
        notification_name: str, config: NotificationsConfig = Depends(get_notifications_config)
):
    try:
        chats = config.get_telegram_notification(notification_name).chats
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)
    return chats


@router.post("/telegram/{notification_name}/chats", status_code=201)
async def create_telegram_notification_chat(
        notification_name: str, data: ChatSchema, config: NotificationsConfig = Depends(get_notifications_config)
):
    try:
        config.add_chat_to_telegram_notification(
            notification_name, chat_id=data.id, chat_name=data.name, description=data.description
        )
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.patch("/telegram/{notification_name}/chats/{chat_id}", status_code=200)
async def update_telegram_notification_chat(
        notification_name: str,
        chat_id: int,
        data: UpdateChatSchema,
        config: NotificationsConfig = Depends(get_notifications_config),
):
    try:
        config.update_chat_to_telegram_notification(
            notification_name, chat_id=chat_id, chat_name=data.name, description=data.description
        )
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.delete("/telegram/{notification_name}/chats/{chat_id}", status_code=204)
async def delete_telegram_notification_chat(
        notification_name: str, chat_id: int, config: NotificationsConfig = Depends(get_notifications_config)
):
    try:
        config.delete_chat_from_telegram_notification(notification_name, chat_id)
    except NotificationsConfig.NotFoundError as exc:
        raise HTTPException(status_code=404, detail=exc.detail)


@router.post("/telegram/{notification_name}/chats/{chat_id}/testMessage", status_code=200)
async def test_telegram_notification(
        notification_name: str,
        chat_id: int,
        config: NotificationsConfig = Depends(get_notifications_config),
):
    tg_bot = TelegramBot(config.get_telegram_notification(notification_name).token)
    try:
        await tg_bot.send_message(chat_id, "Тестовое сообщение")

    except TokenInvalid:
        raise HTTPException(
            status_code=401, detail=f"Неверный токен бота для телеграм оповещения '{notification_name}'"
        )
    except TelegramException as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при отправке тестового сообщения в телеграм оповещение '{notification_name}'"
                   f" для чата '{chat_id}': {exc.detail}",
        )
