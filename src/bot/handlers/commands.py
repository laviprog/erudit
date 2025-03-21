from aiogram import Router, types
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.messages.messages import welcome_message, help_message, about_message, profile_message, message_with_reply_keyboard
from src.services.user import UserService

router = Router()


@router.message(CommandStart())
async def start_command(mes: types.Message, session: AsyncSession):
    service = UserService(session)
    telegram_id = mes.from_user.id

    user = await service.get_by_telegram_id(telegram_id)

    message = await welcome_message(user)
    await message.send(mes)


@router.message(Command("help"))
async def help_command(mes: types.Message):
    message = await help_message()
    await message.send(mes)


@router.message(Command("about"))
async def about_command(mes: types.Message):
    message = await about_message()
    await message.send(mes)


@router.message(Command("profile"))
async def profile_command(mes: types.Message, session: AsyncSession):
    service = UserService(session)
    telegram_id = mes.from_user.id

    user = await service.get_by_telegram_id(telegram_id)

    message = await profile_message(user)
    message_keyboard = await message_with_reply_keyboard()

    await message.send(mes)
    await message_keyboard.send(mes)
