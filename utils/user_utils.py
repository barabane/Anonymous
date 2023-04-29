import re
from loguru import logger


def get_sender_id(data: str) -> str:
    logger.info(re.search('_.*', data).group()[0])

    return re.search('_.*', data).group()[0][1:]
