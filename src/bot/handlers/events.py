from aiogram import Router, F, types
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.messages.messages import event_message, message_with_reply_keyboard
from src.services.event import EventService

router = Router()


@router.message(F.text == "Ближайшие события")
async def events_handler(
        mes: types.Message,
        session: AsyncSession,
):
    service = EventService(session)
    events = await service.get_all()

    if not events:
        message = await event_message()
        await message.send(mes.chat.id)

    else:
        for event in events:
            message = await event_message(event)
            await message.send(mes.chat.id)

    message = await message_with_reply_keyboard()
    await message.send(mes.chat.id)
