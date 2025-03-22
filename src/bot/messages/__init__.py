from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove


class Message:
    def __init__(
            self,
            text: str,
            keyboard: InlineKeyboardMarkup | ReplyKeyboardMarkup | ReplyKeyboardRemove = None,
            image_url: str = None,
    ):
        from src.bot import bot

        self.bot = bot
        self.text = text
        self.keyboard = keyboard
        self.image_url = image_url

    async def send(self, chat_id: int | str) -> int:
        if self.image_url:
            res = await self.bot.send_photo(
                chat_id=chat_id,
                photo=self.image_url,
                caption=self.text,
                reply_markup=self.keyboard,
            )

        else:
            res = await self.bot.send_message(
                chat_id=chat_id,
                text=self.text,
                reply_markup=self.keyboard,
            )

        return res.message_id


async def edit_text_message(chat_id: int | str, message_id: int, edited_text: str) -> None:
    from src.bot import bot

    await bot.edit_message_text(
        chat_id=chat_id,
        message_id=message_id,
        text=edited_text,
    )


async def delete_message(chat_id: int | str, message_id: int):
    from src.bot import bot

    await bot.delete_message(
        chat_id=chat_id,
        message_id=message_id,
    )
