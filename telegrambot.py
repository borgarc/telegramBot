from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import requests

# URL to get the frames of the video
URL = "https://framex-dev.wadrid.net/api/video/Falcon Heavy Test Flight (Hosted Webcast)-wbSwFU6tY1c/frame/"

#URL to send images to telegram bot
TELEGRAM_SEND_PHOTO_URL = "https://api.telegram.org/bot6257775561:AAEe_mya--ZpVroPpV8M2W7KOW8H2b9wYV0/sendPhoto"

# total frames
TOTAL_FRAMES = 61695
FRAME = 0

# Telegram BOT TOKEN
TOKEN = "6257775561:AAEe_mya--ZpVroPpV8M2W7KOW8H2b9wYV0"
updater = Updater("6257775561:AAEe_mya--ZpVroPpV8M2W7KOW8H2b9wYV0", 
                  use_context=True) 
  

def start_command(update: Update, context: CallbackContext):
    update.message.reply_text("Hello!, let's look for the launch frame! (yes/no)")

def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("/start -> to start the bot")
    update.message.reply_text("/restart -> to restart the video")

def custom_command(update: Update,context: CallbackContext):
    global TOTAL_FRAMES, FRAME
    FRAME = 0
    TOTAL_FRAMES = 61695
    update.message.reply_text("Hello!, let's look for the launch frame! (yes/no)")

# Responses

def handle_resonse(text: str) -> str:
    processed: str = text.lower()

    if FRAME == TOTAL_FRAMES:
        return "that's the frame you choose, to restart type /restart"
    else:
        if 'yes' == processed or 'y' == processed or 'n' == processed:
            return "did the rocket launch yet? (y/n)"
        if 'no' == processed:
            return "Bye!"

        return "Only Y or N answers"

def send_image(chat_id, frame):
    url = URL + str(frame)
    print(url)
    params = {
        "chat_id": chat_id,
        "photo": url,
    }

    resp = requests.post(TELEGRAM_SEND_PHOTO_URL, data=params)

def handle_message(update: Update, context: CallbackContext):
    #global TOTAL_FRAMES
    text: str = update.message.text.lower()
    chat_id = update.message.chat.id
    starting_frame = 0
    
    response: str = handle_resonse(text)

    print(f'FRAMES {FRAME}')
    print(f'TOTAL_FRAMES {TOTAL_FRAMES}')

    if text == 'yes':
        starting_frame = random.randint(0, 61695)
        send_image(chat_id, starting_frame)
    elif text == "no":
        update.message.reply_text("if you wanna play type /restart")
    else:
        bisect(text, starting_frame)
        if text == 'y':
            send_image(chat_id, TOTAL_FRAMES)
        else:
            send_image(chat_id, FRAME)


    print(f'BOT RESPONSE {response}')

    update.message.reply_text(response)

def error(update: Update, context: CallbackContext):
    print(f'Update {update} caused error')

def bisect(text, starting_frame):
    """
    Runs a bisection.

    - `text` is the flag to make the bisection
    - `starting_frame` the starting random frame
    """
    global TOTAL_FRAMES, FRAME
    left = FRAME
    right = TOTAL_FRAMES

    mid = int((left + right) / 2)

    if text == 'y':
        if starting_frame == 0:
            TOTAL_FRAMES = mid
        else:
            TOTAL_FRAMES = starting_frame
    if text == 'n':
        if starting_frame == 0:
            FRAME = mid
        else:
            FRAME = starting_frame

if __name__ == '__main__':
    print("STARTING BOT")
    
    # Commands
    updater.dispatcher.add_handler(CommandHandler('start', start_command))
    updater.dispatcher.add_handler(CommandHandler('help', help_command))
    updater.dispatcher.add_handler(CommandHandler('restart', custom_command))

    # Messages
    updater.dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Error
    updater.dispatcher.add_error_handler(error)

    print("POLLING")
    updater.start_polling()

