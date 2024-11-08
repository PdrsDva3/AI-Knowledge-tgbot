from aiogram import Bot, Dispatcher, Router

TOKEN_TG = "your token"
DB_NAME="postgres"
DB_PORT=5432
DB_PASSWORD="postgres"
DB_USER="postgres"
DB_HOST="localhost"


NoneData = ""
# Инициализация бота
bot = Bot(token=TOKEN_TG)
dp = Dispatcher()
router = Router()
