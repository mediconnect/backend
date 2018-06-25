import logging


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("dev_logger")
    logger.setLevel(logging.INFO)

    # create the logging file handler
    fh = logging.FileHandler("dev_except.log")

    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    # add handler to logger object
    logger.addHandler(fh)
    return logger


logger = create_logger()


def exception(_logger):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """
    def _decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                # log the exception
                err = "There was an exception in  "
                err += func.__name__
                _logger.exception(err)

                # re-raise the exception
                raise

        return wrapper
    return _decorator
