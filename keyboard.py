from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_btn = ReplyKeyboardMarkup(resize_keyboard=True)
admin_btn.add(KeyboardButton("Check seeds"), KeyboardButton("Posting"))

kbForSeeds = ReplyKeyboardMarkup(resize_keyboard=True)
cancel = KeyboardButton('Back')

users_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
users_btn.add(KeyboardButton('Profile'), KeyboardButton('Information'), KeyboardButton('Instruction'))
kbForWithdraw = ReplyKeyboardMarkup(resize_keyboard=True)
Withdrawal = KeyboardButton('Withdraw')
kbForWithdraw.add(Withdrawal, cancel)
profile_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
profile_btn.add(KeyboardButton('Set/Change your wallet'), Withdrawal, cancel)
seeds_btn = ReplyKeyboardMarkup(resize_keyboard=True)
seeds_btn.add(KeyboardButton('Delete database'), KeyboardButton('Download database'))
