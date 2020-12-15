from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "+"
OWNER_IDS = [294533591902453760]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False

        self.guild = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all(),

            )
    
    def run(self, version):
        self.VERSION = version

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")
        
    async def on_disconnect(self):
        print("bot disconnected")

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(775380493914996776)
            print("Bot ready")

        else:
            print("Bot reconnected")

    async def on_message(self, message):
        pass

bot = Bot()     