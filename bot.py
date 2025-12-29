import sqlite3
from aiogram import Bot, Dispatcher, executor, types

TOKEN = "PON_AQUI_TU_TOKEN"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = sqlite3.connect("game.db")
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY,
  balance REAL DEFAULT 0,
  last_collect INTEGER DEFAULT 0
)
""")
db.commit()

@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (msg.from_user.id,))
    db.commit()

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton(
        text="🎮 Jugar",
        web_app=types.WebAppInfo(url="PON_AQUI_TU_URL")
    ))

    await msg.answer("Bienvenido al juego", reply_markup=kb)

@dp.message_handler(content_types=["web_app_data"])
async def web_data(msg: types.Message):
    if msg.web_app_data.data == "collect":
        cursor.execute(
            "UPDATE users SET balance = balance + 0.01 WHERE user_id=?",
            (msg.from_user.id,)
        )
        db.commit()
        await msg.answer("💰 Has ganado $0.01")

executor.start_polling(dp)
