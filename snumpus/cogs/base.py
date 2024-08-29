import discord
from discord import app_commands
from discord.ext import commands

from snumpus.utils import LoggableMixin

__all__ = [
    'SnumpusCog',
    'register_cog',
    'get_registered_cogs'
]

_REGISTERED_COGS: list[type(commands.Cog)] = []


class SnumpusCog(commands.Cog, LoggableMixin):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    async def cog_command_error(
            self,
            ctx: commands.Context,
            error: commands.CommandError
    ) -> None:
        self.logger.error(f'An error occurred while handling a command: {error}', exc_info=error)

    async def cog_app_command_error(
            self,
            interaction: discord.Interaction,
            error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandOnCooldown):
            await interaction.response.send_message(str(error), ephemeral=True)

        elif isinstance(error, app_commands.NoPrivateMessage):
            await interaction.response.send_message(f'Command does not work in private messages!')

        elif isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message(f'You do not have permission to do this action!')


def register_cog(enabled: bool = True):
    def inner(cog_cls: type(commands.Cog)):
        _REGISTERED_COGS.append(cog_cls)
        return cog_cls

    return inner


def get_registered_cogs() -> list[type(commands.Cog)]:
    yield from _REGISTERED_COGS
