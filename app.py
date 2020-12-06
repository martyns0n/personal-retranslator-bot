import logging
import os

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardRemove, Update)
from telegram.ext import (CallbackContext, CallbackQueryHandler,
                          CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from telebot.credentials import TOKEN, URL, bot_user_name, chat_id

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

keyboard = [[
    InlineKeyboardButton("Чат Мартына", callback_data='martynomicon'),
    InlineKeyboardButton("Kode Frontenders", callback_data='kode_frontend')
]]
reply_markup = InlineKeyboardMarkup(keyboard)

updater = Updater(TOKEN)

CHOICE, SEND, DONE = range(3)

def entry(update: Update, context: CallbackContext) -> None:
    context.user_data['message_text'] = update.message.text
    context.user_data['chat_id'] = update.message.chat.id
    context.user_data['message_id'] = update.message.message_id

    update.message.reply_text('Please choose:', reply_markup=reply_markup)

    return CHOICE


def choice(update: Update, context: CallbackContext) -> None:
        query = update.callback_query
        print(query)

        context.user_data['channel_id'] = query.data

        print("🚀 ~ file: app.py ~ line 42 ~ context.user_data", context.user_data)

        query.answer()
        query.edit_message_text(text=f"Selected option: {query.data}")

        # return SEND

        # chat_id = user_data.chat_id
        # channel_id = user_data.channel_id
        # message_id = user_data.message_id

        # if user_data.chat_id != 129482161: # id of personal chat with bot
        #     return

        updater.bot.forward_message(chat_id=context.user_data.channel_id, from_chat_id=context.user_data.chat_id, message_id=context.user_data.message_id, disable_notification=True)

# def send(update: Update, context: CallbackContext) -> None:
#     print(context.user_data)
#     user_data = context.user_data
#     # message_text = user_data.message_text
#     chat_id = user_data.chat_id
#     channel_id = user_data.channel_id
#     message_id = user_data.message_id

#     if chat_id != 129482161: # id of personal chat with bot
#         return 
    
#     updater.bot.forwardMessage(chat_id=chat_id, from_chat_id=channel_id, message_id=message_id)

#     return 


def done(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data

    update.message.reply_text(
        f"Until next time!"
    )

    user_data.clear()
    return


def main() -> None:
    dispatcher = updater.dispatcher
    PORT = int(os.environ.get('PORT', '8443'))
    updater.start_webhook(listen="0.0.0.0",
                    port=PORT,
                    url_path=TOKEN)

    botUrl = 'https://{URL}/{HOOK}'.format(URL=URL, HOOK=TOKEN)
    updater.bot.set_webhook(botUrl)

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.text, entry)],
        states={
            CHOICE: [
                CallbackQueryHandler(choice),
            ],
            # SEND: [
            #     CallbackQueryHandler(send)
            # ],
        },
        fallbacks=[CommandHandler('start', done)],
    )

    dispatcher.add_handler(conv_handler)
    # dispatcher.add_handler(MessageHandler(Filters.text, entry))
    # dispatcher.add_handler(CallbackQueryHandler(choice))

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
