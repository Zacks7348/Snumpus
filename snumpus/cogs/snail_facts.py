import json
from pathlib import Path
import random

import discord
from discord import app_commands, Embed, Interaction, Message

from .base import SnumpusCog, register_cog
from snumpus.utils import EmbedColor

__all__ = ['SnailFactsCog']


@register_cog(enabled=True)
class SnailFactsCog(SnumpusCog):
    SNAIL_FACTS_FILE = Path(__file__).parent / 'snail_facts.txt'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SNAIL_FACTS: list[str] = []

        with self.SNAIL_FACTS_FILE.open('r') as f:
            self.SNAIL_FACTS = f.readlines()

    @app_commands.command(name='snailfact', description='Have a snail fact!')
    @app_commands.checks.cooldown(1, 5)
    async def snail_fact(self, interaction: Interaction):
        fact = random.choice(self.SNAIL_FACTS)
        await interaction.response.send_message(fact)
