def _setup_snumpus_bot_logs(console: bool = False):
    import logging
    import logging.handlers
    from pathlib import Path
    log_dir = Path(__file__).parent / 'logs'

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[{asctime}][{levelname}][{name}] {message}', style='{')

    # Logging to File
    snumpus_log_dir = log_dir / 'snumpus-bot'
    snumpus_log_dir.mkdir(exist_ok=True, parents=True)
    log_file = snumpus_log_dir / 'snumpus-bot.log'

    rh = logging.handlers.RotatingFileHandler(str(log_file), maxBytes=512000, backupCount=10, mode='w',
                                              encoding='utf-8')
    rh.setFormatter(formatter)
    rh.setLevel(logging.DEBUG)
    logger.addHandler(rh)

    # Logging to Console
    if console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)
        logger.addHandler(stream_handler)


def _setup_discord_logs(console: bool = False):
    import logging
    import logging.handlers
    from pathlib import Path
    log_dir = Path(__file__).parent / 'logs'

    discord_logger = logging.getLogger('discord')
    discord_logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[{asctime}][{levelname}][{name}] {message}', style='{')

    # Discord logging to file
    discord_log_dir = log_dir / 'discord'
    discord_log_dir.mkdir(exist_ok=True, parents=True)
    log_file = discord_log_dir / 'discord.log'

    rh = logging.handlers.RotatingFileHandler(str(log_file), maxBytes=128000, backupCount=10, mode='w',
                                              encoding='utf-8')
    rh.setFormatter(formatter)
    rh.setLevel(logging.DEBUG)
    discord_logger.addHandler(rh)

    # Discord logging to Console
    if console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        stream_handler.setLevel(logging.DEBUG)
        discord_logger.addHandler(stream_handler)


def init_logging(debug: bool = False, discord: bool = False):
    _setup_snumpus_bot_logs(console=debug)
    _setup_discord_logs(console=discord)
