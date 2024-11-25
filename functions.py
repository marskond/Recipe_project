import os
import sqlite3
import requests

SPOONACULAR_API_KEY = '12313f8e74ba4d3b93ad2980f3135c75'
SPOONACULAR_URL = 'https://api.spoonacular.com/recipes/findByIngredients'

# Функция для поиска рецептов по ингредиентам
def find_recipes(ingredients, num_results=5):
    params = {
        'apiKey': SPOONACULAR_API_KEY,
        'ingredients': ingredients,
        'number': num_results,
        'ranking': 1
    }
    response = requests.get(SPOONACULAR_URL, params=params)
    return response.json()

# Функция для добавления рецепта в базу данных
def save_recipe_to_db(user_id, recipe_id, title, link):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO saved_recipes (user_id, recipe_id, title, link)
        VALUES (?, ?, ?, ?)
    ''', (user_id, recipe_id, title, link))
    conn.commit()
    conn.close()

# Функция для получения сохранённых рецептов
def get_saved_recipes(user_id):
    conn = sqlite3.connect('recipes.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, link FROM saved_recipes WHERE user_id = ?', (user_id,))
    recipes = cursor.fetchall()
    conn.close()
    return recipes