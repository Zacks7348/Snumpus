import discord
from discord.ext.commands import Context, is_owner, command

from .base import SnumpusCog, register_cog

__all__ = ['ManagementCog']


@register_cog(enabled=True)
class ManagementCog(SnumpusCog):

    @command(name='snumpus_bot_sync_cmd_tree')
    @is_owner()
    async def sync_app_commands(self, ctx: Context):
        try:
            self.logger.debug(f'Syncing commands...')
            self._log_cmd_tree()
            commands = await self.bot.tree.sync()
        except Exception:
            self.logger.exception('Could not locally sync commands!')

        await ctx.message.delete()

    @command(name='snumpus_bot_sync_cmd_tree_local')
    @is_owner()
    async def sync_app_commands_local(self, ctx: Context):
        await ctx.message.delete()

        try:
            guild = ctx.guild
            self.logger.debug(f'Syncing commands to Guild with name "{guild}"...')
            self._log_cmd_tree()
            self.bot.tree.clear_commands(guild=guild)
            self.bot.tree.copy_global_to(guild=guild)
            await self.bot.tree.sync(guild=guild)

        except Exception:
            self.logger.exception('Could not locally sync commands!')

    @command(name='snumpus_bot_clear_cmd_tree')
    @is_owner()
    async def clear_app_commands_local(self, ctx: Context):
        await ctx.message.delete()

        try:
            guild = ctx.guild
            self.logger.debug(f'Clearing commands to Guild with name "{guild}"...')
            self._log_cmd_tree()
            self.bot.tree.clear_commands(guild=guild)
            await self.bot.tree.sync(guild=guild)

        except Exception:
            self.logger.exception('Could not locally sync commands!')

    @command(name='snumpus_bot_stop')
    @is_owner()
    async def stop_bot_execution(self, ctx: Context):
        self.logger.info(f'Stopping the bot...')
        await ctx.message.delete()
        await self.bot.close()

    @command(name='listexts')
    async def list_extensions(self, ctx: Context):
        msg = 'Extensions\n'
        for extension_name in self.bot.extensions.keys():
            msg += f'\t{extension_name}\n'
        await ctx.message.delete()
        self.logger.info(msg)

    @command(name='reloadext')
    @is_owner()
    async def reloadext(self, ctx: Context, extension: str):
        await ctx.message.delete()

        try:
            await self.bot.reload_extension(extension)
        except Exception as e:
            self.logger.exception(f'Could not reload extension {extension}: ')
            return

        self.logger.info(f'Extension "{extension}" was reloaded!')

    @command(name='setgame')
    @is_owner()
    async def set_game_activity(self, ctx: Context, game: str):
        await ctx.message.delete()

        activity = discord.Game(game)
        await self.bot.change_presence(activity=activity)
        self.logger.debug(f'Bot activity changed to playing "{game}"')

    def _log_cmd_tree(self, commands=None, prefix: str = 'Command Tree:'):

        log_str = f'{prefix}\n'
        commands = commands or self.bot.tree.walk_commands
        for cmd in commands():
            log_str += f'\t{cmd.name}\n'

        self.logger.debug(log_str)


async def setup(bot):
    await bot.add_cog(ManagementCog(bot))
