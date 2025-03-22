from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.messages import delete_message
from src.bot.messages.messages import create_profile_message, phone_request_message, profile_message, \
    message_with_reply_keyboard, update_profile_message
from src.bot.utils import generate_uuid
from src.database.models import User
from src.services.user import UserService

router = Router()


class UserInfo(StatesGroup):
    full_name = State()
    phone_number = State()


@router.message(F.text == "Создать профиль 📝")
async def start_registration(
        mes: types.Message,
        session: AsyncSession,
        state: FSMContext
):
    service = UserService(session)
    telegram_id = mes.from_user.id

    user = await service.get_by_telegram_id(telegram_id)

    if not user:
        await state.set_state(UserInfo.full_name)

    message = await create_profile_message(user)
    await message.send(mes.chat.id)


@router.message(StateFilter(UserInfo.full_name))
async def process_full_name(
        mes: types.Message,
        state: FSMContext
):
    full_name = mes.text.strip()

    await state.update_data(full_name=full_name)
    await state.set_state(UserInfo.phone_number)

    message = await phone_request_message()
    await message.send(mes.chat.id)


@router.message(StateFilter(UserInfo.phone_number))
async def process_phone_number(
        mes: types.Message,
        session: AsyncSession,
        redis: Redis,
        state: FSMContext
):
    if not mes.contact:
        message = await phone_request_message()
        await message.send(mes.chat.id)
        return

    service = UserService(session)
    data = await state.get_data()

    user = await service.get_by_telegram_id(mes.from_user.id)

    if user:
        user = await service.update(
            user=user,
            full_name=data['full_name'],
            phone_number=mes.contact.phone_number,
        )

    else:
        user = await service.create(
            telegram_id=mes.from_user.id,
            username=mes.from_user.username,
            full_name=data['full_name'],
            phone_number=mes.contact.phone_number,
        )

    callback_id = generate_uuid()
    mes1, mes2 = await send_profile(user, mes.chat.id, callback_id)
    await redis.sadd(callback_id, mes1, mes2)

    await state.clear()

async def send_profile(user: User, chat_id: int | str, callback_id: str):
    message = await profile_message(user, callback_id)
    message_keyboard = await message_with_reply_keyboard()

    return (await message.send(chat_id),
            await message_keyboard.send(chat_id))


@router.callback_query(lambda c: c.data.startswith("edit_profile"))
async def edit_profile(
        callback: types.CallbackQuery,
        redis: Redis,
        state: FSMContext
):
    await state.set_state(UserInfo.full_name)

    message = await update_profile_message()
    await message.send(callback.message.chat.id)

    callback_id = callback.data.split(":")[1]
    mes1, mes2 = await redis.smembers(callback_id)
    await redis.delete(callback_id)
    await delete_message(callback.message.chat.id, mes1)
    await delete_message(callback.message.chat.id, mes2)

    await callback.answer()
