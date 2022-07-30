import Styler
from aiogram import Bot
from os import environ
import message as ms
import logging
import warnings
from config import Token

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO)

BOT_TOKEN = Token

async def style_transfer(message, style_image, content_image):
    new_image = Styler.run(style_image, content_image)

    logging.info(f"Styler Ok")

    tmp_bot = Bot(token=BOT_TOKEN)
    await tmp_bot.send_photo(message.chat.id, photo=new_image)
    
    await tmp_bot.send_message(message.chat.id, "Понравилось?\n Хочешь попробовать еще раз?",
                               reply_markup=ms.algo_keyboard())
    await tmp_bot.close()
