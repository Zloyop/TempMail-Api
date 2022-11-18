import logging
from aiogram import Bot, Dispatcher, executor, types
from TempMailApi import Mailbox
import json
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token='')
dp = Dispatcher(bot)


@dp.message_handler(content_types=['text'])
async def handler(m: types.Message):
	menu = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	menu.add(types.KeyboardButton('✉️ Получить почту'))
	menu.add(types.KeyboardButton('👨‍💻 Скачать код бота'),
			 types.KeyboardButton('🚀 Подробнее о библиотеке'))
	if m.text == '/start':
		await m.answer(f'{m.from_user.full_name}, Приветствую тебя!\nЯ - бот созданый для получения временной почты.\nИспользуй мою клавиатуру, чтобы взаимодействовать со мной', reply_markup=menu)
	elif m.text == '👨‍💻 Скачать код бота':
		await m.reply('Ссылка -> https://github.com/Zloyop/TempMail-Api/blob/main/Bot.py')
	elif m.text == '🚀 Подробнее о библиотеке':
		await m.reply('Ссылка на библиотеку -> https://github.com/Zloyop/TempMail-Api/blob/main/TempMailApi.py')
	elif m.text == '✉️ Получить почту':
		ma = Mailbox('')
		email = f'{ma._mailbox_}@1secmail.com'
		await m.answer(f'📫 Твоя почта: <code>{email}</code>\n\n</b>Почта проверяестся автоматически! Бот оповестит вас, если на почту прийдёт какое-либо письмо!\n\n</i>На 1 почту можно получить только - 1 письмо.</i></b>')
		while True:
			mb = ma.filtred_mail()
			if isinstance(mb, list):
				mf = ma.mailjobs('read',mb[0])
				js = mf.json()
				print(js)
				fromm = js['from']
				theme = js['subject']
				mes = js['textBody']
				await m.answer(f'📩 Новое письмо:\n<b>От:</b> {fromm}\n<b>Тема:</b> {theme}\n<b>Сообщение:</b> {mes}', reply_markup=menu, parse_mode='HTML')
				break
			else:
				pass
			await asyncio.sleep(1)
 

if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True) # Запуск