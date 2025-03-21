from aiogram import Router, types
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_command(sender: types.Message):
    username = sender.from_user.username
    await sender.answer(f"Hello, {username}!")
