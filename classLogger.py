import datetime
import logging


class Logger:
    def __init__(self, source, log_path):
        self.logger = self.logger_init(source, log_path)

    @staticmethod
    def logger_init(source, log_path):
        logger_file = "{}/{}.log".format(log_path, source)
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
