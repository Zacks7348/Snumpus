from discord import __version__
from discord.ext import commands

from .base import SnumpusCog, register_cog

__all__ = ['EventLoggingCog']


@register_cog(enabled=True)
class EventLoggingCog(SnumpusCog):

    @commands.Cog.listener()
    async def on_connect(self):
        self.logger.info('Connected to Discord!')

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.logger.info("Disconnected from Discord!")

    @commands.Cog.listener()
    async def on_ready(self):
        self.logger.info("Connected to {} server(s)".format(
            str(len(self.bot.guilds))))
        self.logger.info("Connected with name: " + self.bot.user.name)
        self.logger.info("Connected with id: " + str(self.bot.user.id))
        self.logger.info("Discord.py Version: " + __version__)


async def setup(bot):
    await bot.add_cog(EventLoggingCog(bot))
