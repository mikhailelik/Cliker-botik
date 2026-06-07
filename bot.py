import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

TOKEN = "ВАШ_ТОКЕН_БОТА"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Хранение очков пользователей
scores = {}


def get_keyboard():
    kb = InlineKeyboardBuilder()
    kb.button(text="👆 Клик!", callback_data="click")
    return kb.as_markup()


@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id

    if user_id not in scores:
        scores[user_id] = 0

    await message.answer(
        f"Ваш счет: {scores[user_id]}",
        reply_markup=get_keyboard()
    )


@dp.callback_query(F.data == "click")
async def click_handler(callback: CallbackQuery):
    user_id = callback.from_user.id

    scores[user_id] = scores.get(user_id, 0) + 1

    await callback.message.edit_text(
        f"Ваш счет: {scores[user_id]}",
        reply_markup=get_keyboard()
    )

    await callback.answer()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())