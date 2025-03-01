import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = "8140848570:AAFRfb6oyrqTHUauNwy8Bq4cIYXPuX2yQvU"

# Функция для подключения к базе данных и получения данных
def get_orders():
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT order_number, image_path FROM your_table WHERE id > 11 and id < 15")
        orders = cursor.fetchall()
        conn.close()
        return orders
    except Exception as e:
        print(f"Ошибка при получении заказов: {e}")
        return []

# Функция для получения имени клиента по номеру заказа
def get_client_name(order_number):
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT client_name FROM your_table WHERE order_number = ?", (order_number,))
        client_name = cursor.fetchone()
        conn.close()
        return client_name[0] if client_name else None
    except Exception as e:
        print(f"Ошибка при получении имени клиента: {e}")
        return None

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    orders = get_orders()
    if not orders:
        await update.message.reply_text('Нет доступных заказов.')
        return

    keyboard = [[InlineKeyboardButton(text=str(order[0]), callback_data=str(order[0])) for order in orders]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите заказ:', reply_markup=reply_markup)

# Обработчик нажатия кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждение нажатия кнопки

    order_number = query.data  # Получаем номер заказа из callback_data
    client_name = get_client_name(order_number)  # Получаем имя клиента по номеру заказа
    orders = get_orders()  # Получаем все заказы для поиска изображения

    # Находим путь к изображению по номеру заказа
    image_path = next((order[1] for order in orders if order[0] == order_number), None)
    print(orders)

    if client_name:
        await query.edit_message_text(text=f"Имя клиента: {client_name}")
        if image_path:
            await context.bot.send_photo(chat_id=query.message.chat_id, photo=open(image_path, 'rb'))
        else:
            await query.edit_message_text(text="Изображение не найдено.")
    else:
        await query.edit_message_text(text="Клиент не найден.")

# Обработчик всех текстовых сообщений
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print(f"Получено сообщение: {update.message.text}")

def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))  # Обработчик нажатий на кнопки
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))  # Обработчик текстовых сообщений

    print("Бот запущен и ожидает сообщений...")  # Лог для подтверждения запуска
    application.run_polling()

if __name__ == '__main__':
    main()
