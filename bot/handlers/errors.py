from aiogram import types, Bot
import logging

logger = logging.getLogger(__name__)

async def catch(event: types.ErrorEvent) -> None:
    """
    Global error handler for unhandled exceptions.
    Logs full error details with traceback.
    """

    logger.error("Unhandled exception occurred", exc_info=event.exception)

    if event.update:
        user_id = event.update.message.from_user.id if event.update.message else "Unknown"
        user_name = event.update.message.from_user.username if event.update.message else "Unknown"
        logger.error(f" | User ID and Name: {user_id}, {user_name}")

    if event.update and event.update.message:
        try:
            await event.update.message.reply("🚨 There was an error. We're working on fixing it!")
        except Exception as message_exception:
            logger.error("Failed to notify user about the error", exc_info=message_exception)