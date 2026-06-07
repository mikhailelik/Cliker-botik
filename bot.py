import os

TOKEN = os.getenv("BOT_TOKEN")
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
ADMIN_ID = 6239728506 # Ваш Telegram ID

WAITING_FOR_MESSAGE = "waiting_for_message"


async def show_menu(message):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
        [InlineKeyboardButton("📩 Связаться с администрацией", callback_data="contact")],
    ]

    await message.reply_text(
        "Выберите вариант:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
        [InlineKeyboardButton("📩 Связаться с администрацией", callback_data="contact")],
    ]

    await update.message.reply_text(
        "Здравствуйте! Выберите вариант:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "info":
        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
        ]

        await query.edit_message_text(
            "Привет, я Геннадий.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "back":
        keyboard = [
            [InlineKeyboardButton("ℹ️ Информация о боте", callback_data="info")],
            [InlineKeyboardButton("📩 Связаться с администрацией", callback_data="contact")],
        ]

        await query.edit_message_text(
            "Здравствуйте! Выберите вариант:",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    elif query.data == "contact":
        context.user_data[WAITING_FOR_MESSAGE] = True

        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="back")]
        ]

        await query.edit_message_text(
            "Напишите сообщение для администрации.",
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

async def receive_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Ответ администратора пользователю

    if update.effective_user.id == ADMIN_ID:

        if update.message.reply_to_message:

            original_text = update.message.reply_to_message.text or ""

            if "USER_ID:" in original_text:

                user_id = int(

                    original_text.split("USER_ID:")[1].split("\n")[0]

                )

                await context.bot.send_message(

                    chat_id=user_id,

                    text=f"📨 Ответ администрации:\n\n{update.message.text}"

                )

                await update.message.reply_text(

                    "✅ Ответ отправлен пользователю."

                )

                return

    # Если пользователь написал не через раздел связи

    if not context.user_data.get(WAITING_FOR_MESSAGE):

        await show_menu(update.message)

        return

    user = update.effective_user

    text = (

        f"USER_ID:{user.id}\n\n"

        f"📨 Новое сообщение\n\n"

        f"От: {user.full_name}\n"

        f"Username: @{user.username}\n"

        f"ID: {user.id}\n\n"

        f"Сообщение:\n{update.message.text}"

    )

    await context.bot.send_message(

        chat_id=ADMIN_ID,

        text=text

    )

    context.user_data[WAITING_FOR_MESSAGE] = False

    await update.message.reply_text(

        "✅ Сообщение успешно отправлено администрации."

    )

    await show_menu(update.message)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_message))
app.run_polling()