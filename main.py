import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, filters, MessageHandler
from dotenv import load_dotenv
import os
import asyncio

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = os.getenv("TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def get_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    currChat = update.effective_chat.id
    messages = [update.effective_message.id]

    newMessage = await context.bot.send_animation(chat_id=update.effective_chat.id, animation=update.message.animation, has_spoiler=True)
    messages.append(newMessage.id)

    newMessage = await context.bot.send_message(chat_id=update.effective_chat.id, text="Forward the spoilered gif to yourself or a friend, because these messages will self-destruct after two minutes.")
    messages.append(newMessage.id)

    await asyncio.sleep(10)

    async def delay_delete(delay=120):
        await asyncio.sleep(delay)
        await context.bot.delete_messages(currChat, messages)

    sleepTask = asyncio.create_task(delay_delete(120))


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    gif_handler = MessageHandler(
        filters.ANIMATION, get_gif)

    application.add_handler(gif_handler)

    application.run_polling()
