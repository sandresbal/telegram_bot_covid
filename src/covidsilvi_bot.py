from config.auth import token
from telegram.ext import Updater, CommandHandler
import requests
import re
from datetime import date

def get_newCases ():
    today = format(date.today())
    contents = requests.get("https://api.covid19tracking.narrativa.com/api/" + today).json()
    newCasesSpain = contents['dates'][today]['countries']['Spain']['today_new_confirmed']
    newCasesMadrid = contents['dates'][today]['countries']['Spain']['regions'][15]['today_new_confirmed']
    data = [newCasesSpain, newCasesMadrid]
    return data 

def send_data (update, context):
    data = get_newCases()
    message = "Hoy los nuevos casos en España son " + str(data[0]) + " y los nuevos casos en Madrid son " + str(data[1])
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id, message)


def main():
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('info',send_data))
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()