import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters, ConversationHandler

TOKEN = "8140848570:AAFRfb6oyrqTHUauNwy8Bq4cIYXPuX2yQvU"

# Определяем состояния
PHOTO, CLIENT_NAME, ORDER_PRICE = range(3)

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

# Обработчик команды /add_order
async def add_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.callback_query.message.reply_text('Я готов принять заказ. Пришлите мне фото товара.')
    
    # Устанавливаем состояние, что пользователь в процессе внесения заказа
    context.user_data['in_order_process'] = True
    
    # Добавляем кнопку "Отменить внесение заказа"
    keyboard = [[InlineKeyboardButton("Отменить внесение заказа", callback_data='cancel_order')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text('Если хотите отменить, нажмите кнопку ниже:', reply_markup=reply_markup)
    
    return PHOTO

# Обработчик получения фото товара
async def receive_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Проверяем, находится ли пользователь в процессе внесения заказа
    if context.user_data.get('in_order_process'):
        if update.message and update.message.photo:
            photo_file = update.message.photo[-1].file_id  # Получаем последнее фото
            context.user_data['photo'] = photo_file  # Сохраняем фото в user_data
            await update.message.reply_text('Фото получено. Теперь отправьте имя клиента.')
            return CLIENT_NAME
        else:
            await update.message.reply_text('Пожалуйста, отправьте фото товара.')
            return PHOTO
    else:
        await update.message.reply_text('Сначала нажмите "Внести заказ".')
        return ConversationHandler.END

# Обработчик получения имени клиента
async def receive_client_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Проверяем, находится ли пользователь в процессе внесения заказа
    if context.user_data.get('in_order_process'):
        context.user_data['client_name'] = update.message.text  # Сохраняем имя клиента
        await update.message.reply_text('Сколько стоил заказ?')
        return ORDER_PRICE
    else:
        await update.message.reply_text('Сначала нажмите "Внести заказ".')
        return ConversationHandler.END

# Обработчик получения стоимости заказа
async def receive_order_price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    order_price = update.message.text
    client_name = context.user_data.get('client_name')
    photo_file = context.user_data.get('photo')

    # Проверяем, что все данные получены
    if client_name and photo_file:
        # Сохранение информации в базу данных
        save_order_to_db(client_name, order_price, photo_file)
        await update.message.reply_text('Заказ успешно внесен!')
    else:
        await update.message.reply_text('Ошибка: Не все данные были получены.')
    
    # Сбрасываем состояние
    context.user_data['in_order_process'] = False
    return ConversationHandler.END

# Функция для сохранения заказа в базу данных
def save_order_to_db(client_name, order_price, photo_file):
    try:
        conn = sqlite3.connect('your_database.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO your_table (client_name, order_price, image_path) VALUES (?, ?, ?)",
                       (client_name, order_price, photo_file))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Ошибка при сохранении заказа: {e}")

# Обработчик команды /track_order
async def track_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Функция получения трек номера еще не реализована.')

# Обработчик команды /unbought_list
async def unbought_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Функция получения списка незакупленного еще не реализована.')

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Внести заказ", callback_data='add_order')],
        [InlineKeyboardButton("Узнать трек номер", callback_data='track_order')],
        [InlineKeyboardButton("Список незакупленного", callback_data='unbought_list')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)

# Обновляем обработчик нажатия кнопки
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()  # Подтверждение нажатия кнопки

    if query.data == 'add_order':
        await add_order(update, context)
    elif query.data == 'track_order':
        await track_order(update, context)
    elif query.data == 'unbought_list':
        await unbought_list(update, context)
    elif query.data == 'cancel_order':
        await cancel_order(update, context)  # Обработка отмены внесения заказа
    else:
        await query.edit_message_text(text="Неизвестная команда.")

# Обновляем main для добавления обработчика текстовых сообщений
def main() -> None:
    application = ApplicationBuilder().token(TOKEN).build()

    # Определяем обработчик разговора
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add_order", add_order)],
        states={
            PHOTO: [MessageHandler(filters.PHOTO, receive_photo)],
            CLIENT_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_client_name)],
            ORDER_PRICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_order_price)],
        },
        fallbacks=[],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))  # Обработчик нажатий на кнопки
    application.add_handler(MessageHandler(filters.PHOTO, receive_photo))  # Обработчик фото

    print("Бот запущен и ожидает сообщений...")  # Лог для подтверждения запуска
    application.run_polling()

if __name__ == '__main__':
    main()
