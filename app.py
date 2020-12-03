import re

import telegram
from flask import Flask, request

from telebot.credentials import URL, bot_token, bot_user_name

global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask(__name__)

@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
  # retrieve the message in JSON and then transform it to Telegram object
  update = telegram.Update.de_json(request.get_json(force=True), bot)

  chat_id = update.message.chat.id
  msg_id = update.message.message_id

  # Telegram understands UTF-8, so encode text for unicode compatibility
  text = update.message.text.encode('utf-8').decode()
  # for debugging purposes only
  print("got text message :", text)
  # the first time you chat with the bot AKA the welcoming message
  if text == "/start":
    # print the welcoming message
    bot_welcome = "Welcome to martyn retranslator bot."
    # send the welcoming message
    bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)


  else:
    try:
      # clear the message we got from any non alphabets
      text = re.sub(r"\W", "_", text)
      # create the api link for the avatar based on http://avatars.adorable.io/
      #  url = "https://api.adorable.io/avatars/285/{}.png".format(text.strip())
      message = "message"
      # reply with a photo to the name the user sent,
      # note that you can send photos by url and telegram will fetch it for you
      bot.sendMessage(chat_id=chat_id,text=message, reply_to_message_id=msg_id)
    except Exception:
      # if things went wrong
      bot.sendMessage(chat_id=chat_id, text="There was a problem in thename you used, please enter different name",reply_to_message_id=msg_id)

    return 'ok'

@app.route('/setWebhook', methods=['GET', 'POST'])
def set_webhook():
   s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"

@app.route('/')
def index():
   return '.'


if __name__ == '__main__':
   app.run(threaded=True)
