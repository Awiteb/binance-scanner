from threading import Thread
import telebot
from binance.client import Client
import time
from datetime import datetime
from pytz import UTC
from tickers import tickers

api_key = str() # your binance api key
api_secret = str() # your binance api secret
client = Client(api_key=api_key, api_secret=api_secret)

chat_id = int() # your telegram id
token = str() # your bot token 
bot = telebot.TeleBot(token)

def pingCommand(message):
    speed = int(datetime.now().timestamp() - datetime.fromtimestamp(message.date).timestamp())
    if (speed < 3):
        typeSpeed = "رائعة 👌🏼"
    elif (speed <= 8):
        typeSpeed = "جيدة  🙁"
    else:
        typeSpeed = "سيئة 👎🏼"
        
    if (speed == 0):
        speed = 'صفر'
        timeName = ''
    elif (speed == 1):
        speed = 'ثانية'
        timeName = ''
    elif (speed == 2):
        speed = "ثانيتين"
        timeName = ''
    elif (speed <= 10):
        timeName = 'ثواني'
    else:
        timeName = 'ثانية'
    bot.reply_to(message, text=f"سرعة البوت {typeSpeed}\nالسرعة: {speed} {timeName}\n⁦")

def scanner():
    for ticker in tickers :
        timestamp = time.time() - 14400
        date = datetime.fromtimestamp(timestamp, tz=UTC).strftime("%d%b, %Y %H:%M")
        try:
            historical = client.get_historical_klines(symbol=ticker, interval='1h', start_str=date)
            quote_volumes = [float(i[7]) for i in historical]
            high = historical[0][2]
            quote_volume = sum(quote_volumes)
            if quote_volume >= 50000000:
                last_hours = '\n'.join([str(i) for i in quote_volumes])
                text = f"{ticker}\n\n{last_hours}\n\nSum: {quote_volume}\n High: {high}"
                bot.send_message(chat_id=chat_id, text=text)
        except IndexError:
            pass
        except Exception as e:
            bot.send_message(chat_id=chat_id, text="ERROR\n\n"+str(e))
    time.sleep(14400)


Thread(target=scanner).start()

@bot.message_handler(commands=['ping'])
def commands_handler(message):
    text = message.text
    if (text.startswith('/ping')):
        pingCommand(message)
    else:
        pass

# Run bot
while True:
    print(f"Start")
    try:
        bot.polling(none_stop=True, interval=0, timeout=0)
    except Exception as e:
        print(e)
        time.sleep(10)