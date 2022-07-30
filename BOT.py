import logging
from aiogram import Bot, Dispatcher, executor, types
import message as ms
import glob
import image_processing
import threading
import asyncio
from os import environ
from config import Token
import warnings
warnings.filterwarnings("ignore")

BOT_TOKEN = Token
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
db_photos = {}
       
class User:
    def __init__(self, user_id):
        self.id = user_id
        self.style_img = 0
        self.type_algo = None

    def restart(self, algo=None):
        self.style_img = 0
        self.type_algo = algo

### start / help ###  
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    db_photos[message.from_user.id] = User(message.from_user.id)
    logging.info(f"Новый Пользователь! Его номер: {len(db_photos)}")
    await message.answer(ms.start_message, reply_markup=ms.start_keyboard())


@dp.callback_query_handler(text="menu")
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.restart()

    await call.message.answer(ms.menu_message, reply_markup=ms.start_keyboard())
    await call.answer()


@dp.callback_query_handler(text="button_style")
async def transfer_style(call: types.CallbackQuery):
    user = db_photos[call.from_user.id]
    user.restart()
    
    await call.message.answer("Мне нужно 2 фотографии. Давай начнем с фотографии стиля, отправь мне ее.\n",
                              reply_markup=ms.style_images())
    await call.answer()


@dp.message_handler(content_types=['photo'])
async def handle_docs_photo(message: types.Message):
    image = message.photo[-1]
    file_info = await bot.get_file(image.file_id)
    photo = await bot.download_file(file_info.file_path)

    user = db_photos[message.from_user.id]
    
    
    if user.style_img == 0:
        user.style_img = photo
        await message.answer("Теперь отправь фотографию, на которую перенести стиль")
    else:
        await message.answer("Необходимо немного подождать")
        logging.info(f"Styler")
        

        threading.Thread(
            target=lambda mess, style_img, content_img:
            asyncio.run(image_processing.style_transfer(mess, style_img, content_img)),
            args=(message, user.style_img, photo)).start()



@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(ms.menu_message, reply_markup=ms.start_keyboard())

async def on_shutdown(dp):
    logging.warning("Выключен..")
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
