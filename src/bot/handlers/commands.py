from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.handlers.profile import send_profile
from src.bot.messages.messages import welcome_message, help_message, about_message, profile_message, message_with_reply_keyboard
from src.bot.utils import generate_uuid
from src.services.user import UserService

router = Router()


@router.message(CommandStart())
async def start_command(mes: types.Message, session: AsyncSession):
    service = UserService(session)
    telegram_id = mes.from_user.id

    user = await service.get_by_telegram_id(telegram_id)

    message = await welcome_message(user)
    await message.send(mes.chat.id)


@router.message(Command("help"))
async def help_command(mes: types.Message):
    message = await help_message()
    await message.send(mes.chat.id)


@router.message(Command("about"))
async def about_command(mes: types.Message):
    message = await about_message()
    await message.send(mes.chat.id)


@router.message(Command("profile"))
async def profile_command(
        mes: types.Message,
        redis: Redis,
        session: AsyncSession
):
    service = UserService(session)
    telegram_id = mes.from_user.id

    user = await service.get_by_telegram_id(telegram_id)

    callback_id = generate_uuid()
    mes1, mes2 = await send_profile(user, mes.chat.id, callback_id)
    await redis.sadd(callback_id, mes1, mes2)
