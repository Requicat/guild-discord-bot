from datetime import datetime 
from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db



PREFIX = "+"
OWNER_IDS = [294533591902453760]


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False

        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

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

    async def rules_reminder(self):
        channel = self.get_channel(775380493914996779)
        await channel.send("Pravidla sem flákni")


    async def on_connect(self):
        print("bot connected")
        
    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        channel = self.get_channel(775380493914996779)
        await channel.send("An error occured")
        raise

    async def on_command_error(self, ctx, ext):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc,"original"):
            raise exc.original

        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            self.ready = True
            self.guild = self.get_guild(775380493914996776)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week="1,3,7", hour=12, minute=0, second=0))
            self.scheduler.start()
            print("Bot ready")

            channel = self.get_channel(775380493914996779)
            

            # embed = Embed(title="Jsem online!", description="Hlídací pes je online.", 
            #               colour=0xFF0000, timestamp=datetime.utcnow())
            # fields = [("Name", "Value", True),
            #           ("Another field", "This field is next to the other one.", True),
            #           ("A non-inline field", "This field will appear on it!s own row", False)]
            # for name, value, inline in fields:                      
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name="Hlídací pes", icon_url=self.guild.icon_url)
            # embed.set_footer(text="This is a footer!")
            # embed.set_thumbnail(url=self.guild.icon_url)
            # embed.set_image(url=self.guild.icon_url)

            # await channel.send(embed=embed)
            #await channel.send(file=File("./data/images"))

            await channel.send("Jsem online!")

        else:
            print("Bot reconnected")

    async def on_message(self, message):
        pass

bot = Bot()     