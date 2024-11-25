from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from handlers import start, view_saved, recommend_recipe, handle_ingredients, save_recipe

TELEGRAM_TOKEN = '7793938959:AAFcCJyvsMAUtr5zDCK2khs6aMqACrSPguY'

# Основная функция для запуска бота
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("saved", view_saved))
    application.add_handler(CommandHandler("recommend", recommend_recipe))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_ingredients))
    application.add_handler(CallbackQueryHandler(save_recipe, pattern="^save_"))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()