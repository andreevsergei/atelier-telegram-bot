from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import json
import os

CHOOSING, TYPING_DESCRIPTION, TYPING_CONTACT, SENDING_PHOTO = range(4)
orders_file = "orders.json"
order_data = {}

keyboard = [["Ремонт", "Вышивка"], ["Пошив", "Задать вопрос"]]

TOKEN = "7667812473:AAEI-RHvESOoBtvoPAIhNCIqyXZgD6IWVsU"
admin_chat_id = 7667812473

def load_orders():
    if os.path.exists(orders_file):
        with open(orders_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_order(order):
    orders = load_orders()
    orders.append(order)
    with open(orders_file, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Добро пожаловать в Ателье 'В новинку'!\nЧто вас интересует?",
        reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return CHOOSING

async def choose_service(update: Update, context: ContextTypes.DEFAULT_TYPE):
    service = update.message.text
    order_data[update.effective_chat.id] = {"service": service}
    await update.message.reply_text("Опишите, пожалуйста, вашу задачу:")
    return TYPING_DESCRIPTION

async def type_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_data[update.effective_chat.id]["description"] = update.message.text
    await update.message.reply_text("Пришлите, пожалуйста, фото или напишите 'Пропустить'.")
    return SENDING_PHOTO

async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1].file_id
    order_data[update.effective_chat.id]["photo"] = photo
    await update.message.reply_text("Оставьте, пожалуйста, номер телефона или Telegram-ник.")
    return TYPING_CONTACT

async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оставьте, пожалуйста, номер телефона или Telegram-ник.")
    return TYPING_CONTACT

async def receive_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    order_data[update.effective_chat.id]["contact"] = update.message.text
    order = order_data[update.effective_chat.id]
    save_order(order)

    message = (
        "Новый заказ:\n"
        f"Услуга: {order['service']}\n"
        f"Описание: {order['description']}\n"
        f"Контакт: {order['contact']}"
    )

    await update.message.reply_text("Спасибо! Мы свяжемся с вами в ближайшее время.")
    await context.bot.send_message(chat_id=admin_chat_id, text=message)
    if 'photo' in order:
        await context.bot.send_photo(chat_id=admin_chat_id, photo=order['photo'])

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Отменено. Если передумаете — просто напишите /start.")
    return ConversationHandler.END

async def list_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.id != admin_chat_id:
        return
    orders = load_orders()
    if not orders:
        await update.message.reply_text("Список заказов пуст.")
        return

    message = "\n\n".join([
        f"{i+1}. Услуга: {o['service']}\nОписание: {o['description']}\nКонтакт: {o['contact']}"
        for i, o in enumerate(orders)
    ])
    await update.message.reply_text("Список заказов:\n\n" + message[:4000])  # Telegram limit

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_service)],
            TYPING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, type_description)],
            SENDING_PHOTO: [
                MessageHandler(filters.PHOTO, receive_photo),
                MessageHandler(filters.TEXT & ~filters.COMMAND, skip_photo),
            ],
            TYPING_CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_contact)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("orders", list_orders))
    app.run_polling()

if __name__ == "__main__":
    main()