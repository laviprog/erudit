from src.bot.messages import Message
from src.bot.messages.keyboards import reply_keyboard, reply_keyboard_create_profile, reply_keyboard_remove, \
    reply_keyboard_phone_number, inline_keyboard_profile_management
from src.database.models import User


async def welcome_message(user: User) -> Message:
    text = "Welcome text"

    if user:
        return Message(
            text=text,
            keyboard=await reply_keyboard()
        )

    return Message(
        text=text,
        keyboard=await reply_keyboard_create_profile()
    )


async def help_message() -> Message:
    return Message(
        text=(
            "Help message"
        ),
        keyboard=await reply_keyboard(),
    )


async def about_message() -> Message:
    return Message(
        text=(
            "About message"
        ),
        keyboard=await reply_keyboard(),
    )


async def profile_message(user: User, callback_id: str) -> Message:
    return Message(
        text=(
            f"Your profile:\n"
            f"Name: {user.full_name}\n"
            f"Phone: {user.phone_number}"
        ),
        keyboard=await inline_keyboard_profile_management(callback_id)
    )


async def message_with_reply_keyboard(
        text: str = "To continue working, click on one of the buttons or commands"
) -> Message:
    return Message(
        text=text,
        keyboard=await reply_keyboard()
    )


async def create_profile_message(user: User) -> Message:
    if user:
        return Message(
            text=(
                "You are already registered, select a command from the menu or one of the buttons below ↓ "
            ),
        )

    return Message(
        text=(
            "Let's start registration!\n"
            "Enter your full name (for example, Ivan Ivanov)"
        ),
        keyboard=await reply_keyboard_remove(),
    )

async def update_profile_message() -> Message:
    return Message(
        text=(
            "Let's start update profile!\n"
            "Enter your full name (for example, Ivan Ivanov)"
        ),
        keyboard=await reply_keyboard_remove(),
    )


async def phone_request_message() -> Message:
    return Message(
        text=(
            "Send your phone number using the button below"
        ),
        keyboard=await reply_keyboard_phone_number(),
    )

