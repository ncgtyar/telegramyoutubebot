import os
import re
import yt_dlp
import ffmpeg
from telegram import *
from telegram.ext import *

config = {
    'quiet': True,
    'default_search': 'ytsearch',
    'extract_flat': '1',
    'noplaylist': True,
    'keepvideo': False,
    'outtmpl': f"X:/yourdirectory/%(title)s",
    'format': 'bestaudio/best',
        'keepvideo': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
}

#For restricting the bot only to specific people. Remove this if you want it to be public
users = [
    0
]

#Add your bot token here
bot = 'yourtoken'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
     if update.message.from_user["id"] in users: #For restricting the bot only to specific people. Remove this if you want it to be public
          await update.message.reply_text("Type what you want to search, it will be downloaded and sent as a .mp3")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
     if update.message.from_user["id"] in users: #For restricting the bot only to specific people. Remove this if you want it to be public
         await update.message.reply_text("⏳ Please wait...")
     
         with yt_dlp.YoutubeDL(config) as ydl:
              search = ydl.extract_info("ytsearch:" + update.message.text, download=False)
              if 'entries' in search:
                  video = search['entries'][0]
                  info_dict = ydl.extract_info("https://www.youtube.com/watch?v=" + video["id"], download=True)
                  file = ydl.prepare_filename(info_dict)
                  await update.message.reply_audio(file + ".mp3")
                  os.remove(file + ".mp3")
              else:
                  update.message.reply_text("⛔ Search failed.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(bot).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), echo))
    
    application.run_polling()
