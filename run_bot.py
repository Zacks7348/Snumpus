import argparse
import asyncio
import os

from snumpus import init_logging
from snumpus.snumpus_bot import start_snumpus


def run_bot():
    parser = argparse.ArgumentParser('Luffy Discord Bot')
    parser.add_argument('--debug', action='store_true', help='Show logs in console')
    parser.add_argument('--discord-logs', action='store_true', help='Show Discord logs in console')
    args = parser.parse_args()
    init_logging(debug=args.debug, discord=args.discord_logs)
    asyncio.run(_main())


async def _main():
    await start_snumpus(os.environ['SNUMPUS_DISCORD_TOKEN'])


if __name__ == '__main__':
    run_bot()
