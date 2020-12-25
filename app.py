"""Code for initiating the bot"""

from dotenv import load_dotenv
from os import getenv
from carica_bot import CaricaBot
from multiprocessing import Process

load_dotenv()
# Variables
BOT_TOKEN = getenv('BOT_TOKEN')


try:
    # CaricaBot.run is a blocking method, thus holding the code when
    # called. In order to avoid that, it is called in a seperate process,
    # thus allowing to process the rest of the code.
    initiate_bot = Process(target=CaricaBot().run, args=(BOT_TOKEN,))
    initiate_bot.start()
except Exception as e:
    print(f'Exception in app.py: {str(e)}')
# initiate_bot.terminate()
print('Done & dusted')
