from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from functions import find_recipes, save_recipe_to_db, get_saved_recipes

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! I can help you find recipes by ingredients. "
        "Just send me a list of ingredients separated by commas.\n\n"
        "Commands:\n"
        "/saved - View saved recipes\n"
        "/recommend - Get daily recipe recommendations"
    )

# Обработчик команды /saved для отображения сохранённых рецептов
async def view_saved(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    saved_recipes = get_saved_recipes(user_id)

    if not saved_recipes:
        await update.message.reply_text("You have no saved recipes.")
    else:
        message = "Your saved recipes:\n\n"
        for title, link in saved_recipes:
            message += f"• [{title}]({link})\n"
        await update.message.reply_text(message, parse_mode='Markdown')

# Обработчик команды /recommend для ежедневных рекомендаций
async def recommend_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    recommended_ingredients = "chicken, rice, tomato"
    recipes = find_recipes(recommended_ingredients, num_results=1)

    if recipes:
        recipe = recipes[0]
        recipe_title = recipe['title']
        recipe_id = recipe['id']
        recipe_link = f"https://spoonacular.com/recipes/{recipe_title.replace(' ', '-')}-{recipe_id}"
        await update.message.reply_text(
            f"Today's recommended recipe:\n\n*{recipe_title}*\n[View Recipe]({recipe_link})",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text("No recommendations available at the moment.")

# Обработчик текстовых сообщений с ингредиентами
async def handle_ingredients(update: Update, context: ContextTypes.DEFAULT_TYPE):
    ingredients = update.message.text
    await update.message.reply_text("Searching for recipes, please wait...")
    recipes = find_recipes(ingredients)

    if not recipes:
        await update.message.reply_text("No recipes found.")
        return

    for recipe in recipes:
        recipe_title = recipe['title']
        recipe_id = recipe['id']
        recipe_link = f"https://spoonacular.com/recipes/{recipe_title.replace(' ', '-')}-{recipe_id}"
        keyboard = [
            [InlineKeyboardButton("Save Recipe", callback_data=f"save_{recipe_id}_{recipe_title}")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"*{recipe_title}*\n[View Recipe]({recipe_link})",
            parse_mode='Markdown',
            reply_markup=reply_markup
        )

# Обработчик для сохранения рецепта
async def save_recipe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data.split('_')
    recipe_id = data[1]
    recipe_title = data[2]
    user_id = query.from_user.id
    recipe_link = f"https://spoonacular.com/recipes/{recipe_title.replace(' ', '-')}-{recipe_id}"
    
    save_recipe_to_db(user_id, recipe_id, recipe_title, recipe_link)
    await query.answer("Recipe saved!")
    await query.edit_message_text(text=f"{recipe_title} saved to your recipes!")