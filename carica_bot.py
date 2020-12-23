"""Main code for the Carica-Bot
"""

import discord

class CaricaBot(discord.Client):
    """CaricaBot class that extends the discord.Client class
    & overwrites the methods of the extended class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        """Print bot details & send User details to the 'caricare' channel
        when bot is ready.
        """
        print(f'Logged in as {self.user.name} - {self.user.id}')
        print('------')