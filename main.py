import telebot
from scrape import search_for_concerts
import sys

TOKEN = sys.argv[1]

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    '''
    Sends messege on (start).
            Parameters:
                    None
            Returns:
                    None
    '''
    bot.send_message(m.chat.id, 'Этот бот создан для быстрого поиска концертов твоих любимых исполнителей. Всё, что требуется сделать, - это ввести исполнителя.')

def resultstring(concert):
    '''
    Converts concert information from dict to string
            Parameters:
                    concert (dict) : input information
            Returns:
                    Information as string for pasting
    '''
    parameters = 'Название : ' + concert['name'] + '\n'
    parameters += 'Когда : ' + concert['date'] + '\n'
    parameters += 'Место : ' + concert['place'] + '\n'
    parameters += concert['adress'] + '\n'
    parameters += 'Стоимость : ' + concert['price'] + ' р.' + '\n'
    parameters += 'Ссылка : ' + concert['url'] + '\n\n'
    return parameters

@bot.message_handler(content_types=["text"])
def handle_text(message):
    '''
    Reacts on input text
            Parameters:
                    message (string) : input text
            Returns:
                    None
    '''
    concerts = search_for_concerts(message.text)
    if len(concerts) == 0:
        bot.send_message(message.chat.id, 'Не могу увидеть совпадения, концертов нет. Проверь написание')
    else:
        s = ''
        for concert in concerts:
            s += resultstring(concert)
        bot.send_message(message.chat.id, 'Самое похожее, что мне удалось найти :\n\n' + s)





bot.polling(none_stop=True, interval=0)

