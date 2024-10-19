from config import PRINT_DEBUG, LOG_DEBUG
import sys
import logging

# ロギングの設定
logging.basicConfig(
    # ログファイルのパスを指定
    filename='log/app.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

# エラーログファイル専用のハンドラーを追加
error_handler = logging.FileHandler('log/error.log')  # エラーログファイルのパス
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

# ロガーを設定
logger = logging.getLogger()
logger.addHandler(error_handler)


def print_error(message: str) -> None:
    """デバッグメッセージを出力する。DEBUGがTrueの場合のみ表示。"""
    # print(message)
    print(message, file=sys.stderr)
    logger.error(message)

def print_debug(message: str) -> None:
    """デバッグメッセージを出力する。DEBUGがTrueの場合のみ表示。"""
    if PRINT_DEBUG:
        print(message)

def log_debug(message: str) -> None:
    """ """
    if LOG_DEBUG:
        logging.debug(message)
    # if LOG_DEBUG:
    #     print(message)