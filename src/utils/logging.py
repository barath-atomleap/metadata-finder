import coloredlogs
from logging.config import dictConfig
from utils.config import get_config


def configure_logging():
  logging_config = get_config('logging')
  standard_format = logging_config['formatters']['standard']
  dictConfig(logging_config)
  coloredlogs.install(fmt=standard_format['format'], datefmt=standard_format['datefmt'])