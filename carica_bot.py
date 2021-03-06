"""Main code for the Carica-Bot
"""

import discord
from platform import uname
from asyncio import sleep
from charge_info import checkBattery, getCheckInterval, readBattery

class CaricaBot(discord.Client):
    """CaricaBot class that extends the discord.Client class
    & overwrites the methods of the extended class
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channel_name: str = 'caricare'
        self.caricare_channel: discord.TextChannel = None
        # create the background task and run it in the background
        self.battery_status_task = self.loop.create_task(self.batteryStatus())
    

    async def getChannel(self) -> discord.TextChannel:
        """Retrieve the caricare channel for the bot to communicate in.

        Returns
        -------
        - discord.TextChannel
            - Instance of the text channel for the bot
        
        Raises
        ------
        - ChannelNotFound
        - ChannelNotCreated
        """
        
        # If the property: caricare_channel is not null, that implies that it 
        # contains instance of the caricare channel, 
        # then return the channel instance
        if(self.caricare_channel != None):
            return self.caricare_channel
        
        # Server is referred to as a Guild in the API
        # Assumming that the bot was invited to only one server,
        # the first element retrieved from the list is considered to send
        # the messages to
        try:
            guild : discord.Guild = self.guilds[0]
            for channel in guild.channels:
                if(channel.name == self.channel_name and channel.type == discord.ChannelType.text):
                    self.caricare_channel = channel
                    return channel
        except Exception as e:
            raise ChannelNotFound(self.channel_name, str(e))

        # If channel doesn't exist, then create one
        try:    
            self.caricare_channel = await guild.create_text_channel(self.channel_name)
            return self.caricare_channel
        except Exception as e:
            raise ChannelNotCreated(self.channel_name, str(e))


    async def on_ready(self):
        """Print bot details & send User details to the 'caricare' channel
        when bot is ready.
        """

        # Print client details
        # TODO: Change print to log
        print(f'Logged in as {self.user.name} - {self.user.id}')
        print('------')

        # Retrieve the channel for the bot
        channel = await self.getChannel()
        # Send user machine details to the channel
        system_details = uname()
        await channel.send(
            'Carica-Bot at your service! :robot:\n' + 
            f'Logged in from a **{system_details.system}** system ' + 
            f'with username: **{system_details.node}**'
        )
        print('Login message sent') # TODO: Convert print to log
    

    async def on_message(self, message:discord.Message):
        """Respond when message received from the user

        Parameters
        ----------
        - message : `discord.Message`
            - Instance of the message received

        Raises
        ------
        - MessageNotSent
            - Raise custom Exception when `discord.TextChannel.send` throws an Exception
        """

        # Avoid the message, if the bot itself is the author of the message
        if message.author == self.user:
            return
        
        # Respond when summoned
        try:
            # Command to start a chat with the bot
            invoke_command: str = '!crc'
            # Retrieve the message content
            msg: str = message.content

            # Check if the message starts with the invoke bot command
            if msg.startswith(invoke_command):
                # Seperate the actual command purpose from the invoke command prefix
                command = msg.removeprefix(invoke_command).strip()
                
                # Say Hello if no command passed
                if (command == ''):
                    await self.caricare_channel.send(
                        content = f'Hello, {message.author.display_name}! :wave:', 
                        delete_after = 2*60.0
                    )
                # Provide the battery status for the said commands
                elif (command == '?' or command == 'status'):
                    battery = readBattery()
                    percent = battery['percentage']
                    chargingStatus = 'charging' if(battery['isCharging']) else 'discharging'
                    await self.caricare_channel.send(
                        content = f'**Battery Status**:\nBattery charge is at *{percent}%* & is *{chargingStatus}* now.', 
                        delete_after = 2*60.0
                    )
        except Exception as e:
            raise MessageNotSent(str(e))
    

    async def close(self):
        """Send a Goodbye message & logs out the bot.

        discord.Client.logout() method could have been overriden, however, after
        reading the API docs, it turns out that the 'logout' method is an alias
        to the actual 'close' method. The method closes all websocket connections
        of the bot to Discord. Before the bot is logged out, it sends a final
        goodbye message to denote that the bot has logged out.

        NOTE: This method might not be called, if the program is terminated
        abruptly. Thus, the bot will be shown offline in the server/guild as the
        connections are broken, but the Goodbye message won't be received.

        Raises
        ------
        - MessageNotSent
            - Custom exception for failure in message sending
        """
        try:
            if(self.caricare_channel):
                await self.caricare_channel.send('Bye, bye! :wave:')
        except Exception as e:
            raise MessageNotSent(str(e))
        await super().close()


    async def batteryStatus(self):
        """Check the battery status & send message to the channel"""

        await self.wait_until_ready()
        # While the bot is connected
        while not self.is_closed():
            percent = 100
            # Check if the instance of the channel exists
            if(self.caricare_channel):
                # Retrieve battery status
                battery_status = checkBattery()
                # Check if the user is to be notified
                # (Read checkBattery docs to understand)
                if(battery_status['msg']):
                    percent, msg = battery_status['percent'], battery_status['msg']
                    msg += f' \nBattery: {percent}%'
                    # Send the message to the channel
                    await self.caricare_channel.send(msg)
            
            # Retrieve interval for sleep
            await sleep(getCheckInterval(percent) * 60.0)


def activateCaricaBot(BOT_TOKEN: str) -> None:
    carica_bot = CaricaBot()
    carica_bot.run(BOT_TOKEN)

# Exceptions
ChannelNotFound = lambda name, error : Exception(f'Error in carica_bot: getChannel - Could not find {name} channel\n{error}')
ChannelNotCreated = lambda name, error: Exception(f'Error in carica_bot: getChannel - Could not create {name} channel\n{error}')
MessageNotSent = lambda error: Exception(f'Error in carica_bot: on_message - Could not send message\n{error}')
