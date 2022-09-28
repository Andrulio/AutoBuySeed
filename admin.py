from aiogram import Bot, types
from aiogram.dispatcher.filters import Text

from config import dp, seeds, bot, admin
from keyboard import admin_btn, seeds_btn


@dp.message_handler(Text(equals='Check seeds'))
async def check_seeds(message: types.Message):
    list_of_seeds = []
    sep = '\n'
    lines = seeds.find()
    for line in lines:
        list_of_seeds.append(f"<code>{line['_id']}</code>\n")
    await bot.send_message(admin, f"{sep.join(list_of_seeds)}", parse_mode='HTML', reply_markup=seeds_btn)

@dp.message_handler(Text(equals='Delete database'))
async def del_base(message: types.Message):
    lines = seeds.find()
    for line in lines:
        seeds.delete_one({'_id': line['_id']})
    await bot.send_message(admin, 'Succesfully deleted database!', reply_markup=admin_btn)

@dp.message_handler(Text(equals='Download database'))
async def del_base(message: types.Message):
    lines = seeds.find()
    list_of_seeds = []
    sep = "\n"
    for line in lines:
        list_of_seeds.append(line['_id'])
    with open('seeds.txt', 'a+') as t:
        t.write(sep.join(list_of_seeds))
    await bot.send_document(admin, open('seeds.txt', 'rb'), caption='Succesfully downloaded database!')
