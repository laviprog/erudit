from aiogram import Router, F, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.messages.messages import create_profile_message, phone_request_message, profile_message, \
    message_with_reply_keyboard
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
    await message.send(mes)


@router.message(StateFilter(UserInfo.full_name))
async def process_full_name(
        mes: types.Message,
        state: FSMContext
):
    full_name = mes.text.strip()

    await state.update_data(full_name=full_name)
    await state.set_state(UserInfo.phone_number)

    message = await phone_request_message()
    await message.send(mes)


@router.message(StateFilter(UserInfo.phone_number))
async def process_phone_number(
        mes: types.Message,
        session: AsyncSession,
        state: FSMContext
):
    if not mes.contact:
        message = await phone_request_message()
        await message.send(mes)
        return

    service = UserService(session)
    data = await state.get_data()

    user = await service.create(
        telegram_id=mes.from_user.id,
        username=mes.from_user.username,
        full_name=data['full_name'],
        phone_number=mes.contact.phone_number,
    )

    message = await profile_message(user)
    message__keyboard = await message_with_reply_keyboard()
    await message.send(mes)
    await message__keyboard.send(mes)

    await state.clear()
