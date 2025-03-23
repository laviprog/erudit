from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove


async def reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Ближайшие события"),
                KeyboardButton(text="Мои заявки"),
            ]
        ],
        resize_keyboard=True,
    )


async def reply_keyboard_create_profile():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Создать профиль 📝")
            ]
        ],
        resize_keyboard=True,
    )


async def reply_keyboard_phone_number():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Send a phone number", request_contact=True)
            ]
        ],
        resize_keyboard=True,
    )


async def inline_keyboard_profile_management(callback_id: str):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Изменить профиль", callback_data=f"edit_profile:{callback_id}")],
    ])


async def inline_keyboard_for_event_registration(event_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Зарегистрироваться",
                    callback_data=f"register_event:{event_id}"
                )
            ],
        ]
    )


async def inline_keyboard_for_application_management(application_id: int):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✏️ Изменить заявку", callback_data=f"edit_application:{application_id}")],
        [InlineKeyboardButton(text="❌ Удалить заявку", callback_data=f"delete_application:{application_id}")],
    ])


async def reply_keyboard_remove():
    return ReplyKeyboardRemove()
