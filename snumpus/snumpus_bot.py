import logging

import discord
from discord.ext import commands
from discord import Intents

from snumpus.cogs import get_registered_cogs


class SnumpusBot(commands.Bot):
    """Wumpus, but snail"""

    def __init__(self):
        intents = Intents.all()
        activity = discord.Game('Snail Simulator')
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, activity=activity)


async def start_snumpus(token: str):
    log = logging.getLogger(__name__)

    log.debug('Initialing bot...')
    bot = SnumpusBot()

    for cog_cls in get_registered_cogs():
        cog = cog_cls(bot)
        await bot.add_cog(cog)

    log.info('Starting bot...')
    await bot.start(token)

    log.info('Bot event loop closed: bot was stopped!')
