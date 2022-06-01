import telebot
from config import keys, TOKEN
from extensions import ConvertionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(content_types=['photo','document','audio',"sticker", "video", "video_note", "location", "contact", ])
def content_answer(message: telebot.types.Message):
    bot.reply_to(message, 'Это очень здорово и интересно, но давай вернемся к валютам!')

@bot.message_handler(content_types=['voice', ])
def voice_answer(message: telebot.types.Message):
    bot.reply_to(message, 'У тебя красивый голос, теперь вернемся к валютам!')

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = "чтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \ " \
    "<в какую валюту перевести> \ " \
    "<количество переводимой валюты>\nУвидеть список доступных валют: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "список доступных валют:"
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionExeption("Неверные параметры ввода")
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionExeption as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"не удалось обработать команду\n{e}")
    else:
        text = f'цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)