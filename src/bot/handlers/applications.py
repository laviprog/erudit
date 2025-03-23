from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.messages.messages import message_with_reply_keyboard, application_message
from src.services.application import ApplicationService

router = Router()


@router.message(F.text == "Мои заявки")
async def applications_handler(
        mes: types.Message,
        session: AsyncSession,
):
    app_service = ApplicationService(session)
    telegram_id = mes.from_user.id

    applications = await app_service.get_all_by_telegram_id(telegram_id)

    if not applications:
        message = await application_message()
        await message.send(mes.chat.id)

    else:
        for application in applications:
            message = await application_message(application)
            await message.send(mes.chat.id)

    message = await message_with_reply_keyboard()
    await message.send(mes.chat.id)


class RegisterTeam(StatesGroup):
    team_name = State()
    team_size = State()
