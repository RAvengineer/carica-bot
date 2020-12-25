"""Code for initiating the bot"""

from dotenv import load_dotenv
from os import getenv
from carica_bot import activateCaricaBot
from multiprocessing import Process
from charge_info import checkBattery, notify, getCheckInterval
from time import sleep

load_dotenv()
# Variables
BOT_TOKEN = getenv('BOT_TOKEN')

# Discord bot setup
try:
    # CaricaBot.run is a blocking method, thus holding the code when
    # called. In order to avoid that, it is called in a seperate process,
    # thus allowing to process the rest of the code.
    initiate_bot = Process(target=activateCaricaBot, args=(BOT_TOKEN,))
    initiate_bot.start()
except Exception as e:
    print(f'Exception in app.py: {str(e)}')
# initiate_bot.terminate()  # For future reference


# System notification setup
while(True):
    msg, percent = checkBattery().values()
    if(msg):
        msg = msg[:msg.find(':')]
        msg += f' Battery: {percent}%'
        notify(msg)
    # Pause the processing for some time
    sleep(getCheckInterval(percent) * 60.0)
