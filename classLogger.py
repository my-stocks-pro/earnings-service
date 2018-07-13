import datetime
import logging


class Logger:
    def __init__(self, source):
        self.logger = self.logger_init(source)

    @staticmethod
    def logger_init(source):
        logger_file = "app_logs/{}_{}.log".format(source, datetime.datetime.now().strftime("%Y-%m-%d"))
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        file_handler = logging.FileHandler(logger_file)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def to_logger(self, **kwargs):
        for name, value in kwargs.items():
            if name == "error":
                self.logger.error(value)
            if name == "info":
                self.logger.info(value)

    def mark_date_log(self, type):
        date_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.to_logger(info=["{} PARSER -> {}".format(type, date_now)])
