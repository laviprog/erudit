from src.bot.messages import Message
from src.bot.messages.keyboards import reply_keyboard, reply_keyboard_create_profile, reply_keyboard_remove, \
    reply_keyboard_phone_number, inline_keyboard_profile_management, inline_keyboard_for_event_registration, \
    inline_keyboard_for_application_management
from src.database.models import User, Event, Application, Status


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


async def event_text(event: Event) -> str:
    return (
        f"📅 {event.event_time.strftime('%d.%m.%Y %H:%M')} - {event.title}\n"
        f"📍 {event.location}\n"
        f"📝 {event.description or 'Без описания'}"
    )


async def event_message(event: Event = None) -> Message:
    if not event:
        return Message(
            text=(
                "К сожалению, событий нет. Мы обязательно вам сообщим о новых событиях!"
            ),
        )

    return Message(
        text=await event_text(event),
        keyboard=await inline_keyboard_for_event_registration(event.id),
        image_url=event.image_url,
    )


async def application_text(application: Application) -> str:
    STATUS_LABELS = {
        Status.APPROVED: "✅ Подтверждена",
        Status.PENDING: "⏳ Ожидает подтверждения",
        Status.DECLINED: "❌ Отклонена",
    }
    status = STATUS_LABELS.get(application.status, "⚠ Неизвестный статус")

    return await event_text(application.event) + '\n\n' +(
        f"📌 Ваша заявка на это событие:\n"
        f"Название команды: {application.team_name}\n"
        f"Количество участников: {application.team_size}\n"
        f"Статус: {status}"
    )


async def application_message(application: Application = None) -> Message:
    if not application:
        return Message(
            text=(
                "На текущий момент у вас нет заявок на события!"
            ),
        )

    return Message(
        text=await application_text(application),
        keyboard=await inline_keyboard_for_application_management(application.id),
    )
