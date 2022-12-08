''' 로깅시스템 테스트용 코드
# -*- coding: utf-8 -*-
import logging.handlers


class Setting:
    """로거 세팅 클래스
        ::
            Setting.LEVEL = logging.INFO # INFO 이상만 로그를 작성
    """
    LEVEL = logging.DEBUG
    FILENAME = "xingapi.log"
    MAX_BYTES = 10 * 1024 * 1024
    BACKUP_COUNT = 10
    FORMAT = "%(asctime)s[%(levelname)s|%(name)s,%(lineno)s] %(message)s"


def Logger(name):
    """파일 로그 클래스
        :param name: 로그 이름
        :type name: str
        :return: 로거 인스턴스
        ::
            logger = Logger(__name__)
            logger.info('info 입니다')
    """

    # 로거 & 포매터 & 핸들러 생성
    logger = logging.getLogger(name)
    formatter = logging.Formatter(Setting.FORMAT)
    streamHandler = logging.StreamHandler()
    fileHandler = logging.handlers.RotatingFileHandler(
        filename=Setting.FILENAME,
        maxBytes=Setting.MAX_BYTES,
        backupCount=Setting.BACKUP_COUNT)

    # 핸들러 & 포매터 결합
    streamHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 로거 & 핸들러 결합
    logger.addHandler(streamHandler)
    logger.addHandler(fileHandler)

    # 로거 레벨 설정
    logger.setLevel(Setting.LEVEL)

    return logger
'''

'''
### log를 세팅 해주는 단계입니다.
# logging 모듈 import
import logging


def get_logger(name=None):
    # 1 logger instance를 만듭니다.
    logger = logging.getLogger(name)

    # 2 logger의 level을 가장 낮은 수준인 DEBUG로 설정합니다.
    logger.setLevel(logging.DEBUG)

    # 3 formatter 지정하여 log head를 구성해줍니다.
    ## asctime - 시간정보
    ## levelname - logging level
    ## funcName - log가 기록된 함수
    ## lineno - log가 기록된 line
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - [%(funcName)s:%(lineno)d] - %(message)s")

    # 4 handler instance 생성하여 console 및 파일로 저장할 수 있도록 합니다. 파일명은 txt도 됩니다.
    console = logging.StreamHandler()
    file_handler_debug = logging.FileHandler(filename="log_debug.log")
    file_handler_info = logging.FileHandler(filename="log_info.log")

    # 5 handler 별로 다른 level 설정합니다. 설정한 level 이하 모두 출력,저장됩니다.
    console.setLevel(logging.INFO)
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_info.setLevel(logging.INFO)

    # setLevel 정보
    console.setLevel(logging.INFO)
    file_handler_debug.setLevel(logging.DEBUG)
    file_handler_info.setLevel(logging.INFO)

    # 6 handler 출력을 format 지정방식으로 합니다.
    console.setFormatter(formatter)
    file_handler_debug.setFormatter(formatter)
    file_handler_info.setFormatter(formatter)

    # 7 logger에 handler 추가합니다.
    logger.addHandler(console)
    logger.addHandler(file_handler_debug)
    logger.addHandler(file_handler_info)

    # 8 설정된 log setting을 반환합니다.
    return logger
'''
'''
import logging

class MyFilter(object):
    def __init__(self, level):
        self.__level = level

    def filter(self, logRecord):
        return logRecord.levelno <= self.__level

#create a logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler('mylog.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
#set filter to log only ERROR lines
handler.addFilter(MyFilter(logging.ERROR))
logger.addHandler(handler)

logger.error('This is an ERROR message')
logger.critical('This is an CRITICAL message')
'''

'''
import sys
import logging
import logging.handlers

from rich.logging import RichHandler

LOG_PATH = "./log.log"
RICH_FORMAT = "[%(filename)s:%(lineno)s] >> %(message)s"
FILE_HANDLER_FORMAT = "[%(asctime)s]\\t%(levelname)s\\t[%(filename)s:%(funcName)s:%(lineno)s]\\t>> %(message)s"

def set_logger() -> logging.Logger:
    logging.basicConfig(
        level="NOTSET",
        format=RICH_FORMAT,
        handlers=[RichHandler(rich_tracebacks=True)]
    )
    logger = logging.getLogger("rich")

    file_handler = logging.FileHandler(LOG_PATH, mode="a", encoding="utf-8")
    file_handler.setFormatter(logging.Formatter(FILE_HANDLER_FORMAT))
    logger.addHandler(file_handler)

    return logger

def handle_exception(exc_type, exc_value, exc_traceback):
    logger = logging.getLogger("rich")

    logger.error("Unexpected exception",
                 exc_info=(exc_type, exc_value, exc_traceback))

if __name__ == "__main__":
    logger = set_logger()
    sys.excepthook = handle_exception

    for i in range(3, -1, -1):
        num = 1/i
        logger.info(f"1/{i} = {num}")
'''

'''
# 로그 생성
logger = logging.getLogger()

# 로그의 출력 기준 설정
logger.setLevel(logging.INFO)

# log 출력 형식
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# log 출력
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# log를 파일에 출력
file_handler = logging.FileHandler('my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

for i in array:
	logger.info(f'{i}번째 방문입니다.')'''