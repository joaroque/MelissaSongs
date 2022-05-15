import os
import asyncio
from decouple import config
from telebot.async_telebot import AsyncTeleBot

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.messages import Message as msg
from utils.downloader import downloader
from utils.yt_search import search as music_search
from utils.shazam_search import search as voice_search


TELEGRAM_TOKEN = config('TOKEN')
VOICE_DIR = config('VOICE_DIR')
AUDIO_DIR = config('AUDIO_DIR')

# stickers
sucess_st = "CAACAgIAAxkBAAIBFWKA-BbERtjxIIMk6WyBV5l8UOe6AAItAQACMNSdERCGBLkvnsTRJAQ"
error_st = "CAACAgIAAxkBAAIBGmKA-e1XoWNI3v9qMohWrXOfMyioAAIsAQACMNSdEbJU5DcKWA99JAQ"
search_st = "CAACAgIAAxkBAAIBHGKA-naJPWwqlEPnzCEq10MyaSXdAAIVAQACMNSdEW7uekmzNU5CJAQ"

bot = AsyncTeleBot(TELEGRAM_TOKEN, parse_mode=None)


# message sender 
async def sender(chat_id, content, msg_id=None, parse_mode=None, f=None):
	if msg_id:
		return await bot.edit_message_text(text=content,
										   chat_id=chat_id,
							               message_id=msg_id, 
							               parse_mode=parse_mode)
	# send audio
	if f:
		return await bot.send_audio(chat_id, content)

	return await bot.send_message(chat_id=chat_id,
						          text=content, 
						          parse_mode=parse_mode)



# Send the welcome and help message
@bot.message_handler(commands=['start'])
async def send_welcome(message):
	await bot.reply_to(message, msg.start.format(message.from_user.first_name))


# Send the welcome and help message
@bot.message_handler(commands=['help'])
async def send_welcome(message):
	await bot.reply_to(message, msg.helpp)


# Handles all sent music title
@bot.message_handler(commands=['music'])
async def handle_music_search(message):
	chat_id = message.chat.id
	search = await sender(chat_id, msg.searching)
	sticker = await bot.send_sticker(chat_id, search_st)
	if message.text:
		
		res = music_search(message.text)
		
		if res[0] == False:
			err = res[1]
			
			await sender(chat_id, msg.err[err], search.message_id)
			await bot.delete_message(chat_id, sticker.message_id)
			
			sticker = await bot.send_sticker(chat_id, error_st)

		else:
			await bot.delete_message(chat_id, sticker.message_id)
			
			text = f"{res[2]}\n{res[1]}"
			await sender(chat_id, text, search.message_id)
			
			sticker = await bot.send_sticker(chat_id, sucess_st)	
			await sender(chat_id, msg.downloading)

			file_path = downloader(AUDIO_DIR, res[2], res[1])
			if file_path:
				with open(file_path, 'rb') as file:
					await bot.delete_message(chat_id, sticker.message_id)
					await sender(message.chat.id, file, f=True)
				# DELETE DOWLOANDED AUDIO FILE
				os.remove(file_path)
	else:
			await sender(chat_id, msg.err['not_found'], search.message_id)
			await bot.delete_message(chat_id, sticker.message_id)
			sticker = await bot.send_sticker(chat_id, error_st)


	
# Handles all sent voice
@bot.message_handler(content_types=['voice'])
async def handle_voice(message):
	chat_id = message.chat.id
	search = await sender(chat_id, msg.searching)
	sticker = await bot.send_sticker(chat_id, search_st)
	
	file_info = await bot.get_file(message.voice.file_id)
	file = await bot.download_file(file_info.file_path)
	
	file_name = file_info.file_id + ".oga"

	with open(VOICE_DIR+file_name, 'wb') as new_file:
		new_file.write(file)
	
	res = await voice_search(VOICE_DIR, file_name)
	# REMOVE DOWNLOADED VOICE FILE
	os.remove(VOICE_DIR+file_name)
	
	if res[0] == False:
		await bot.delete_message(chat_id, sticker.message_id)
		err = res[1]
		await sender(chat_id, msg.err[err], search.message_id)
		sticker = await bot.send_sticker(chat_id, error_st)
	else:
		await bot.delete_message(chat_id, sticker.message_id)
		text = f"{res[2]}\n{res[1]}"
		await sender(chat_id, text, search.message_id)
		
		sticker = await bot.send_sticker(chat_id, sucess_st)	
		await sender(chat_id, msg.downloading)

		file_path = downloader(AUDIO_DIR, res[2], res[1])
		if file_path:
			with open(file_path, 'rb') as file:
				await sender(message.chat.id, file, f=True)
				await bot.delete_message(chat_id, sticker.message_id)
				# DELETE DOWLOANDED AUDIO FILE
				os.remove(file_path)


def main():
	asyncio.run(bot.infinity_polling())


if __name__ == "__main__":
	main()

