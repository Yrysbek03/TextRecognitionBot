import telebot
from config import token
import cv2
import pytesseract
from PIL import Image


# initialization bot
bot=telebot.TeleBot(token)

# handler for start
@bot.message_handler(commands=['reg','start'])
def start_bot(message):
    bot.send_message(message.chat.id, 'Send your photo')

# echo for any text and audio files
@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['audio'])
def echoff(message):
    bot.send_message(message.chat.id, message.text)

# handler for start recognition 
@bot.message_handler(content_types=['document'])
def obrobotka(message):
    try:
        chat_id = message.chat.id
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = 'PATH/TO/YOUR/FOLDER' + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, 'Wait! Scanning in progress...')


        f_name= message.document.file_name

        img = cv2.imread(f_name)
        ret, t_img = cv2.threshold(img, 116, 250, 1)

        # if windows
        pytesseract.pytesseract.tesseract_cmd = r'PATH\TO\tesseract.exe'
        
        # setting up the tesseract
        custom_config = r'--oem 3 --psm 6'

        bot.send_message(message.chat.id, "If white")

        text = pytesseract.image_to_string(img, lang='eng', config=custom_config)
        bot.send_message(message.chat.id, text)

        bot.send_message(message.chat.id, "If black")

        text = pytesseract.image_to_string(t_img, lang='eng', config=custom_config)
        bot.send_message(message.chat.id, text)


    except Exception as e:
        bot.send_message(message.chat.id, 'Че та ошибка🧐\nвозможно файл слишком большой🤔')
        bot.send_message(message.chat.id, e)

if __name__ == '__main__':
    bot.polling(none_stop=True)


