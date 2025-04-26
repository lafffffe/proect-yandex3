import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram import ReplyKeyboardMarkup

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def pinterest(update, context):
    await update.message.reply_text("скинь ссылку на изображение pinterest")


async def youtube(update, context):
    await update.message.reply_text("скинь ссылку на изображение youtube")


async def tiktok(update, context):
    await update.message.reply_text("скинь ссылку на изображение tiktok")


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я умею скачивать видео по ссылке",
        reply_markup=markup
    )


async def help_command(update, context):
    await update.message.reply_text("Я пока не умею помогать...")


def main():
    application = Application.builder().token('7801940292:AAEEDCLRZO0f4vzTJyzEgOMNSpxQWwB-k3Q').build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(CommandHandler("pinterest", pinterest))
    application.add_handler(CommandHandler("youtube", youtube))
    application.add_handler(CommandHandler("tiktok", tiktok))

    application.run_polling()


reply_keyboard = [['/pinterest', '/youtube', '/tiktok']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

if __name__ == '__main__':
    main()
