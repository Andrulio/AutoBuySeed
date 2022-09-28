import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from pymongo import MongoClient

min_value_to_withdraw = 5
admin = 0  # admin telegram id
value_per_one_seed = 3  # value per 1 seed, in $

bot = Bot("#")  # bot token
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
cluster = MongoClient(
    "#")     # mongodb
# link
db = cluster["base"]
users = db['users']
blocked = db['blocked']
seeds = db['seeds']
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())
