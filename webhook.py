import logging

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.executor import start_webhook

from config import data as params

API_TOKEN = params.TOKEN_API
WEBHOOK_HOST = params.WEBHOOK_HOST
WEBHOOK_PATH = params.WEBHOOK_PATH
WEBHOOK_URL = params.WEBHOOK_URL
WEBAPP_HOST = params.WEBAPP_HOST
WEBAPP_PORT = params.WEBAPP_PORT

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())


class CheckStatesGroup(StatesGroup):
    photo = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(text=params.start_message)
    await message.delete()
    await CheckStatesGroup.photo.set()


@dp.message_handler(lambda message: not message.photo, state=CheckStatesGroup.photo)
async def validate_photo(message: types.Message) -> None:
    await message.reply("It's not a picture, resend it!")


@dp.message_handler(content_types=['document'], state=CheckStatesGroup.photo)
async def validate_file(message: types.Message) -> None:
    await message.reply("This is a file, need to send a photo, resend it!")


@dp.message_handler(content_types=['photo'], state=CheckStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext) -> None:
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
        await bot.send_photo(chat_id=params.ADMIN_ID,
                             photo=data['photo'],
                             caption=f'User: @{message.from_user.username}, '
                                     f'Full_name: {message.from_user.full_name} send photo!')

        await bot.send_photo(chat_id=params.MASTER_ID,
                             photo=data['photo'],
                             caption=f'User: @{message.from_user.username}, '
                                     f'Full_name: {message.from_user.full_name} send photo!')

    await message.reply(f'Thanks for the payment!\n\n'
                        f'Send request to our private group {params.private_instagram_group} '
                        f'💜\n\nWelcome to the club!💜')
    await state.finish()


async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL)
    logging.info('Bot starting successfuly!')


async def on_shutdown(_):
    logging.warning('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning('Bye!')


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
