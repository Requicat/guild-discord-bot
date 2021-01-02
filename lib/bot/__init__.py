from asyncio import sleep

from datetime import datetime
from glob import glob

from discord import Intents
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import Embed
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

from ..db import db



PREFIX = "+"
OWNER_IDS = [294533591902453760]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print(f"{cog} cog ready")

    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])



class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = Ready()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX, 
            owner_ids=OWNER_IDS,
            intents=Intents.all(),

            )

    def setup(self):
        for cog in COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"{cog} cog is loaded")

        print("setup complete")
    
    def run(self, version):
        self.VERSION = version

        print("running setup...")
        self.setup()

        with open("./lib/bot/token.0", "r", encoding="utf-8") as tf:
            self.TOKEN = tf.read()

        print("Running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def rules_reminder(self):
        await self.stdout.send("Pravidla sem flákni")


    async def on_connect(self):
        print("bot connected")
        
    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        await self.stdout.send("An error occured")
        raise

    async def on_command_error(self, ctx, ext):
        if isinstance(exc, CommandNotFound):
            pass

        elif hasattr(exc,"original"): #Shows original exception, way more cleaner 
            raise exc.original

        else:
            raise exc #Shows a lot of shits in case we don't have original exception path

    async def on_ready(self):
        if not self.ready:
            self.guild = self.get_guild(775380493914996776)
            self.stdout = self.get_channel(775380493914996779) #Standart output with channel ID, use instead of "channel = self.get_channel(###-###-###)" for every instance
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week="0,2,6", hour=12, minute=0, second=0))
            self.scheduler.start()

            await self.stdout.send("Jsem online!")

            

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

            while not self.cogs_ready.all_ready():
                await sleep(0.5)

            self.ready = True
            print("Bot ready")

            

        else:
            print("Bot reconnected")

    async def on_message(self, message):
        pass

bot = Bot()     