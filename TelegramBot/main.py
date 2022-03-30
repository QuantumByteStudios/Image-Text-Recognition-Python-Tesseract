from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import constants
import pytesseract
import os
import logging
import platform
import cv2

try:
    from PIL import Image
except ImportError:
    import Image

BOT_KEY = "ApniBotKeyDaal"

the_updater = Updater(BOT_KEY,
                      use_context=True)


def universalClear():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")


def the_start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    name = update.message.from_user.first_name
    update.message.reply_text('Hello! '+name + constants.welcome_text)
    print('New User Login: '+name)


def the_help(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text("/start : to start the bot")


def convert_image(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    try:
        file_id = update.message.photo[-1].get_file()
        img_name = str(chat_id)+'.png'
        file_id.download(img_name)

        image = cv2.imread(img_name)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Performing OTSU threshold
        ret, thresh1 = cv2.threshold(
            gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))

        # Applying dilation on the threshold image
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

        # Finding contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)

        # Creating a copy of image
        im2 = image.copy()
        firstFetchText = pytesseract.image_to_string(im2)

        # First Fetch
        # print(firstFetchText)

        # extracted_sting = (pytesseract.image_to_string(Image.open(img_name)))

        if firstFetchText:
            update.message.reply_text(
                ''+str(firstFetchText)+'\n\nImage-Text Generation: TextifyBot', reply_to_message_id=update.message.message_id)
        else:
            update.message.reply_text(constants.no_text_found)

    except Exception as e:
        update.message.reply_text("Error Occurred: "+str(e)+"")

    finally:
        try:
            os.remove(img_name)
        except Exception:
            pass


def reply_to_text_message(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(constants.reply_to_text_message)


def main():
    """Start the bot."""
    universalClear()


# adding the handler to handle the messages and commands
the_updater.dispatcher.add_handler(CommandHandler('start', the_start))
the_updater.dispatcher.add_handler(CommandHandler('help', the_help))
# Filtering out unknown commands
the_updater.dispatcher.add_handler(MessageHandler(
    Filters.text & ~Filters.command, reply_to_text_message))
the_updater.dispatcher.add_handler(MessageHandler(
    Filters.photo & ~Filters.command, convert_image))

# running the bot
the_updater.start_polling()
