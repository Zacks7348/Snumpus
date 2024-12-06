from pathlib import Path
import random
import re


from bs4 import BeautifulSoup
import discord
from discord import app_commands, Embed, Interaction, Message
import requests
import urllib

from .base import SnumpusCog, register_cog
from snumpus.utils import EmbedColor

__all__ = ['SnailImageCog']


@register_cog(enabled=True)
class SnailImageCog(SnumpusCog):
    SNAIL_SEARCH_PHRASES_FILE = Path(__file__).parent / 'snail_image_search_phrases.txt'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SNAIL_SEARCH_PHRASES: list[str] = []

        with self.SNAIL_SEARCH_PHRASES_FILE.open('r') as f:
            self.SNAIL_SEARCH_PHRASES = f.readlines()

    @app_commands.command(name='snimage', description='Have a snail image!')
    @app_commands.checks.cooldown(1, 5)
    async def snail_image_command(self, interaction: Interaction):
        url_img = self._search_for_image()
        if url_img is None:
            embed = Embed(
                title='Could not find a snail image! Please try again later.',
                colour=EmbedColor.RED
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

        await interaction.response.send_message(url_img)

    def _search_for_image(self):
        try:
            # Choose a random search phrase
            search_phrase = random.choice(self.SNAIL_SEARCH_PHRASES)

            # Make it suitable for URL
            url_keyword = urllib.parse.quote_plus(search_phrase)

            # Make the URL
            url = f'https://www.google.com/search?hl=jp&q={url_keyword}&btnG=Google+Search&tbs=0&safe=off&tbm=isch'
            headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }

            # Make the request
            response = requests.get(url, headers=headers)

            # Cook up some soup
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find the img tag
            find_el = soup.find_all('img')

            # Extract the text
            txt = find_el[1]
            match = re.search(r'src=".*"', str(txt), flags=0)
            if match:
                return match.group().replace('src=', '').replace('"', '')

            return None

        except Exception:
            self.logger.exception(f'An error occurred while fetching a snail image: ')
            return None
