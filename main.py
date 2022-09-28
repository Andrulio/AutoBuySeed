# SPECIAL FOR GITHUB
from aiogram.dispatcher import FSMContext

from config import *
from keyboard import *
from states import *
from admin import *
from aiogram import executor, types
from aiogram.dispatcher.filters import Text

# --------------------------------START---------------------------------------------
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id == admin:
        await message.answer('Welcome to Admin Panel! Choose the next action', reply_markup=admin_btn)
    elif users.count_documents({"_id": message.chat.id}) == 0:
        users.insert_one({"_id": message.chat.id, "seeds": 0, "balance": 0})
        await message.answer(f'Hi! Send me file with seeds\n'
                             f'Price per 1 seed: {value_per_one_seed} $',
                             reply_markup=users_btn)
    else:
        await message.answer(f'Hi! Send me file with seeds\n'
                             f'Price per 1 seed: {value_per_one_seed} $',
                             reply_markup=users_btn)

# ----------------------------------USER PART---------------------------------------
@dp.message_handler(Text(equals='Profile'))
async def balance(message: types.Message):
    user = users.find_one({'_id': message.chat.id})
    balances = user['balance']
    pcs = user['seeds']
    await bot.send_message(message.chat.id,
                           f'🍬<b>Your seeds</b>: {pcs} pieces\n'
                           f'💰<b>Balance</b> <code>{balances}$</code> \n'
                           f'⚙<b>Wallet</b>: <code>{user["wallet"]}</code>\n'
                           f'📄<b>Minimum to withdraw</b> {min_value_to_withdraw} $',
                           reply_markup=profile_btn, parse_mode='HTML')

@dp.message_handler(Text(equals='Set/Change your wallet'))
async def wallet_changer(message: types.Message):
    await bot.send_message(message.chat.id, "Type your wallet to change:")
    await wallet.wallet_change.set()

@dp.message_handler(state=wallet.wallet_change)
async def wallet_changer_state(message: types.Message, state: FSMContext):
    print(message.text)
    users.find_one_and_update({"_id": message.chat.id},
                              {"$set": {
                                  "wallet": message.text}})
    await bot.send_message(message.chat.id, f"Your wallet has changed to: {message.text}")
    await state.finish()
@dp.message_handler(Text(equals='Back'))
async def cancel(message: types.Message):
    await bot.send_message(message.chat.id, 'Main menu', reply_markup=users_btn)


@dp.message_handler(Text(equals='Withdraw'))
async def withdraw(message: types.Message):
    if users.find_one({'_id': message.chat.id})['balance'] < 5:
        await bot.send_message(message.chat.id, f"Balance is lower than {min_value_to_withdraw}$")
    else:
        await bot.send_message(message.chat.id, 'Type the value to withdraw: ')


@dp.message_handler(Text(equals='Information'))
async def info(message: types.Message):
    await bot.send_message(message.chat.id, 'Admin @Andrulio\nCreator @Andrulio')


@dp.message_handler(content_types=["document"])     # processing file of txt seed-phrases
async def handle_text(message: types.Message):
    await bot.send_message(admin, 'New seed-phrases you have!')
    file = await bot.get_file(message.document.file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"received/{message.chat.id}")
    with open(f"received/{message.chat.id}", 'r') as f:
        content = f.readlines()
        lines = [line.rstrip('\n') for line in content]
    already = 0
    pcs = 0
    for line in lines:
        if seeds.count_documents({"_id": line}) == 0:
            seeds.insert_one({"_id": line})
            pcs += 1
        else:
            already += 1
    await bot.send_message(message.chat.id, f"Checked: {len(lines)}\n"
                                            f"Already we have: {already}\n"
                                            f"Good: {pcs}")
    users.find_one_and_update({"_id": message.chat.id},
                              {"$set": {
                                  "seeds": int(users.find_one({"_id": message.chat.id})["seeds"]) + pcs}})


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
