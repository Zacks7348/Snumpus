import json
from pathlib import Path
import random

import discord
from discord import app_commands, Embed, Interaction, Message
from discord.ext.commands import Cog

from .base import SnumpusCog, register_cog
from snumpus.utils import EmbedColor

__all__ = ['SnailifyCog']


@register_cog(enabled=True)
class SnailifyCog(SnumpusCog):
    CONFIG_FILE = Path(__file__).parent / 'snailify_config.json'

    VOWELS = ('a', 'e', 'i', 'o', 'u')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with self.CONFIG_FILE.open('r') as f:
            self.config = json.load(f)
            self.webhook_id = None

    @Cog.listener()
    async def on_message(self, message: Message) -> None:
        if (
                message.channel.id != self.config['snailChannel'] or
                (message.webhook_id == self.webhook_id and self.webhook_id is not None) or
                message.author.id == self.bot.user.id
        ):
            return

        snail_content = self.snailify(message.content)
        if snail_content != message.content:
            self.logger.debug(f'Snailifying worked! Editing message...')
            try:

                webhooks = await message.channel.webhooks()
                webhook = discord.utils.find(lambda wh: wh.user == self.bot.user, webhooks)

                if webhook is None:
                    self.logger.debug(f'Creating new webhook')
                    webhook = await message.channel.create_webhook(name=self.bot.user.name)

                if webhook.id != self.webhook_id:
                    self.logger.debug(f'Updating cached webhook ID ({self.webhook_id} -> {webhook.id})')
                    self.webhook_id = webhook.id

                # Get attachments
                attachments = []
                for attachment in message.attachments:
                    try:
                        attachment_file = await attachment.to_file()
                        attachments.append(attachment_file)

                    except Exception as e:
                        self.logger.error(f'Could not download attachment "{attachment}! Ignoring..."')
                        continue

                await webhook.send(
                    content=snail_content,
                    username=message.author.display_name,
                    avatar_url=message.author.display_avatar.url,
                    wait=True,
                    embeds=message.embeds,
                    files=attachments,
                    silent=True
                )

                await message.delete()

            except Exception as e:
                self.logger.exception(f'Could not send message: {e}')

    @app_commands.command(name='setsnailchance', description='Set the snail chance')
    @app_commands.describe(chance='The percentage chance to snail (i.e. 60%)')
    async def set_snail_chance(self, interaction: Interaction, chance: str):
        if not chance[-1].endswith('%'):
            embed = Embed(
                title='Chance must be a percentage (i.e. 60%)!',
                colour=EmbedColor.RED
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        try:
            chance = float(chance[:-1])

        except Exception:
            embed = Embed(
                title='Chance must be a percentage (i.e. 60%)!',
                colour=EmbedColor.RED
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.config['snailifyChance'] = chance / 100
        self._save_config()
        embed = Embed(
            title=f'Snail chance updated to {chance * 100}% ({chance})!',
            colour=EmbedColor.GREEN
        )
        await interaction.response.send_message(embed=embed)
        return

    @app_commands.command(name='setsnailchannel', description='Set the snail channel')
    @app_commands.describe(channel_id='The channel ID for the snails to snail')
    async def set_snail_chance(self, interaction: Interaction, channel_id: str):
        try:
            channel = interaction.guild.get_channel(int(channel_id))
        except Exception:
            embed = Embed(
                title=f'No channel found with ID {channel_id}!',
                colour=EmbedColor.RED
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        if channel is None:
            embed = Embed(
                title=f'No channel found with ID {channel_id}!',
                colour=EmbedColor.RED
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.config['snailChannel'] = channel_id
        self._save_config()
        embed = Embed(
            title=f'Snail channel updated to {channel.mention}!',
            colour=EmbedColor.GREEN
        )
        await interaction.response.send_message(embed=embed)
        return

    def snailify(self, message: str) -> str:
        """/Snailify [message]"""
        self.logger.debug(f'Snailfying message: \n{message}')
        if not message or message.startswith('https:'):
            self.logger.debug(f'Ignoring non message')
            return message

        new_message = []
        prev_word = None
        for word in message.split():
            try:
                new_message.append(self.snailify_word(word, prev_word, self.config['snailifyChance']))
            except Exception as e:
                self.logger.error(f'Could not snailify word "{word}": {e}')
                new_message.append(word)
            prev_word = word

        snail_message = ' '.join(new_message)
        self.logger.debug(f'Snailified:\n\t{message}\n\t{snail_message}')
        return snail_message

    def snailify_word(self, word: str, prev_word: str | None, chance: float):
        # Don't snailify words that are 2 characters or less
        if len(word) <= 3:
            return word

        if not word[0].isalpha() or not word[1].isalpha():
            return word

        # Chance for snail
        if prev_word is not None and prev_word.lower() in ('a', 'is', 'the'):
            chance += 0.1

        r = random.random()
        if r > chance:
            return word

        s = 's' if not word[0].isupper() else 'S'
        n = 'n' if not word[1].isupper() else 'N'
        sn = s + n
        # If the 2nd character is a vowel only replace the first character with "sn"
        if word[0].lower() in self.VOWELS:
            return sn + word

        elif word[1].lower() in self.VOWELS:
            return sn + word[1:]

        return sn + word[2:]

    def _read_config(self) -> dict:
        with self.CONFIG_FILE.open('r') as f:
            return json.load(f)

    def _save_config(self) -> None:
        with self.CONFIG_FILE.open('w') as f:
            self.logger.debug(f'Saving config:\n{json.dumps(self.config, indent=4)}')
            return json.dump(self.config, f, indent=4)
