from config import PRINT_DEBUG, LOG_DEBUG

def print_error(message: str) -> None:
    """デバッグメッセージを出力する。DEBUGがTrueの場合のみ表示。"""
    print(message)

def print_debug(message: str) -> None:
    """デバッグメッセージを出力する。DEBUGがTrueの場合のみ表示。"""
    if PRINT_DEBUG:
        print(message)
        
def log_debug(message: str) -> None:
    """ """
    if LOG_DEBUG:
        print(message)