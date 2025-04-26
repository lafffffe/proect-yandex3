import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Устанавливаем уровень логгирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Функция для обработки команды /sendfile
def send_file(update: Update, context: CallbackContext) -> None:
    chat_id = update.effective_chat.id
    file_path = 'path/to/your/file.txt'  # Укажите путь к вашему файлу
    with open(file_path, 'rb') as file:
        context.bot . send_document(chat_id, document=file)

# Основная функция
def main() -> None:
    # Ваш токен, полученный у BotFather
    updater = Updater("7801940292:AAEEDCLRZO0f4vzTJyzEgOMNSpxQWwB-k3Q")
    # Получаем диспетчер для регистрации обработчиков
    dispatcher = updater.dispatcher
    # Регистрируем обработчик команды /sendfile
    dispatcher.add_handler(CommandHandler("sendfile", send_file))
    # Запускаем бот
    updater.start_polling()

if __name__ == '__main__':
    main()
