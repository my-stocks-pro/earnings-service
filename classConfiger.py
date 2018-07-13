import yaml


class Configer:
    def __init__(self, conf_path):
        self.config = self.read_config(conf_path)

    @staticmethod
    def read_config(conf_path):
        with open(conf_path, 'r') as file:
            return yaml.load(file)
