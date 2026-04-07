import logging

def get_logger(name):
    """Логгер (только консоль)"""
    logger = logging.getLogger(name)
    """Вариант 1: Только INFO (для обычного запуска)"""
    """"Вариант 2: DEBUG (для отладки, когда что-то пошло не так)"""
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%H:%M:%S'
        ))
        logger.addHandler(handler)

    return logger