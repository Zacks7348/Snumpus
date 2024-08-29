import logging


class EmbedColor:
    RED = 0xFF0000
    GREEN = 0x7CFC00
    GREY = 0x23272A
    BLURPLE = 0x7289dA
    YELLOW = 0xFFF000


class LoggableMixin:
    @classmethod
    def create_logger(cls, name: str = None, suffix: str = None):
        name = name or cls.__name__
        log_name = f'{cls.__module__}.{name}'
        if suffix is not None:
            log_name += f'.{suffix}'
        return logging.getLogger(log_name)

    @property
    def logger(self):
        return self.create_logger()
