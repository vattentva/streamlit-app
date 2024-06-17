import logging

def setup():
    logging.basicConfig(
        format='%(asctime)s - %(message)s',
        level=logging.INFO,
        handlers=[
            logging.FileHandler("log/app.log"),
            logging.StreamHandler()
        ]
    )
    logging.info("logging config setup")