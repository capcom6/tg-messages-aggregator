import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s",
    )


setup_logging()