import logging
from datetime import datetime
import pytz

def setup():
    logging.basicConfig(
        level=logging.DEBUG,  # デバッグレベルの設定
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # ログのフォーマット
        handlers=[
            logging.StreamHandler()  # コンソールへの出力
        ]
    )
    # ロガーを取得
    logger = logging.getLogger(__name__)
    logging.info("logging config setup")

    return logger

def _info(msg):
    logging.info(msg)

def _error(msg):
    logging.error(msg)

