import logging


def get_basic_logger():
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Set up format for the logs
    formatter = logging.Formatter(
        "%(levelname)s-%(asctime)s %(filename)s:%(lineno)s -"
        " %(funcName)2s()\n%(message)s \n"
    )

    # Setup Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    # Add the console handler to the logger object
    logger.addHandler(console_handler)
    logger.propagate = False

    return logger
