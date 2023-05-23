from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']

app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "https://devapi.qweather.com/v7/weather/now?location=101010100&key=a5d75526455f47158bbacf1189b356db"
  res = requests.get(url).json()
  weather = res['now']
  return weather['text']  , weather['temp']

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

def judgment_length(e):
    length = len(e)
    words = words1 = words2 = words3 = words4 = words5 = words6 = ''
    if length <= 20:
        words = e
    elif 20 < length <= 40:
        words = e[0:20]
        words1 = e[20:39]
    elif 40 < length <= 60:
        words = e[0:20]
        words1 = e[20:39]
        words2 = e[40:59]
    elif 60 < length <= 80:
        words = e[0:20]
        words1 = e[20:39]
        words2 = e[40:59]
        words3 = e[60:79]
    elif 80 < length <= 100:
        words = e[0:20]
        words1 = e[20:39]
        words2 = e[40:59]
        words3 = e[60:79]
        words4 = e[80:99]
    elif 100 < length <= 120:
        words = e[0:20]
        words1 = e[20:39]
        words2 = e[40:59]
        words3 = e[60:79]
        words4 = e[80:99]
        words5 = e[100:119]
    elif 120 < length <= 140:
        words = e[0:20]
        words1 = e[20:39]
        words2 = e[40:59]
        words3 = e[60:79]
        words4 = e[80:99]
        words5 = e[100:119]
        words6 = e[120:139]
    return [words, words1, words2, words3, words4, words5, words6]
  
def get_words():
  global total_data
  words = requests.get("https://api.shadiao.pro/chp")
  data = words.json()['data']['text']
  total_data = judgment_length(data)
  print('total_data',total_data)
  if words.status_code != 200:
    return get_words()
  return total_data

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)

get_words()

client = WeChatClient(app_id, app_secret)
# "love_days":{"value":get_count()},
wm = WeChatMessage(client)
wea, temperature = get_weather()
data = {"weather":{"value":wea},"temperature":{"value":temperature},"birthday_left":{"value":get_birthday()},"words":{"value":total_data[0]},"words1":{"value":total_data[1]},"words2":{"value":total_data[2]},"words3":{"value":total_data[3]},"words4":{"value":total_data[4]},"words5":{"value":total_data[5]},"words6":{"value":total_data[6]},}

res = wm.send_template(user_id, template_id, data)
print('words',data)
print(res)
