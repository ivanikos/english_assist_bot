import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

import openai_logic

# Replace 'YOUR_BOT_TOKEN' with your bot's token
API_TOKEN = os.getenv("ENG_ASSIST_TOKEN")

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Command handler for /start
@dp.message(Command(commands=["start"]))
async def send_welcome(message: types.Message):
    await message.answer("Hello! I'm your group assistant bot. I am here to help!")

# Message handler for group and supergroup chats
@dp.message()
async def echo(message: types.Message):
    user_message = message.text
    print(user_message)
    print(message.chat.id)
    print(message.chat.title)
    print(message.is_topic_message)
    print(message.message_thread_id)
    # Check if the message is from a group or supergroup
    if str(message.message_thread_id) == "387":
        response = openai_logic.gpt_request(user_message)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        await message.answer(response)


# Main function to run the bot
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
