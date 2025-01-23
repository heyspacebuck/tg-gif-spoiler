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


async def get_media(update: Update, context: ContextTypes.DEFAULT_TYPE, mediaType: str):
    async def delay_delete(delay=120):
        await asyncio.sleep(delay)
        await context.bot.delete_messages(currChat, messages)

    currChat = update.effective_chat.id
    messages = [update.effective_message.id]

    if mediaType == "gif":
        newMessage = await context.bot.send_animation(chat_id=currChat, animation=update.message.animation, has_spoiler=True)
        messages.append(newMessage.id)
    elif mediaType == "photo":
        newMessage = await context.bot.send_photo(chat_id=currChat, photo=update.message.photo[0].file_id, has_spoiler=True)
        messages.append(newMessage.id)
    elif mediaType == "video":
        newMessage = await context.bot.send_video(chat_id=currChat, video=update.message.video.file_id, has_spoiler=True)
        messages.append(newMessage.id)
    else:
        await asyncio.sleep(2)
        await context.bot.delete_messages(currChat, messages)
        return

    newMessage = await context.bot.send_message(chat_id=currChat, text=f"Forward the spoilered {mediaType} to yourself or a friend, because these messages will self-destruct after two minutes.")
    messages.append(newMessage.id)

    async def delay_delete(delay=120):
        await asyncio.sleep(delay)
        await context.bot.delete_messages(currChat, messages)

    sleepTask = asyncio.create_task(delay_delete(120))


async def get_gif(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_media(update, context, "gif")


async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_media(update, context, "photo")


async def get_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_media(update, context, "video")


async def discard_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await get_media(update, context, "deer")


if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()

    # start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    gif_handler = MessageHandler(
        filters.ANIMATION, get_gif)
    photo_handler = MessageHandler(filters.PHOTO, get_photo)
    video_handler = MessageHandler(filters.VIDEO, get_video)
    remainder_handler = MessageHandler(
        ~(filters.PHOTO | filters.VIDEO | filters.ANIMATION), discard_post)

    application.add_handler(gif_handler)
    application.add_handler(photo_handler)
    application.add_handler(video_handler)
    application.add_handler(remainder_handler)

    application.run_polling()
