import logging
from datetime import datetime
import pytz

def setup():
    logging.basicConfig(
        level=logging.INFO,  # デバッグレベルの設定
        format='%(asctime)s - %(levelname)s - %(message)s',  # ログのフォーマット
        datefmt='%Y-%m-%d %H:%M:%S',  # タイムスタンプのフォーマット
        handlers=[
            logging.StreamHandler()  # コンソールへの出力
        ]
    )
    # ロガーを取得
    logger = logging.getLogger(__name__)
    logger.info("logging config setup")

    return logger

def _info(msg):
    logging.info(msg)

def _error(msg):
    logging.error(msg)

