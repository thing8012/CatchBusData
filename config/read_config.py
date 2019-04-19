import os
import yaml


class SystemConfig():
    def __init__(self, config_name=None):
        if not config_name:
            self.path = os.path.join(os.path.dirname(__file__), 'system.yaml')
        else:
            self.path = os.path.join(os.path.dirname(__file__), config_name)
        self.data = dict()

    def get_config(self, path=None):
        if not path:
            if os.path.exists(self.path):
                with open(self.path, 'r', encoding='utf8') as stream:
                    try:
                        self.data = yaml.load(stream)
                        return self.data
                    except yaml.YAMLError as exc:
                        print(exc)
                        return dict()
        else:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf8') as stream:
                    try:
                        self.data = yaml.load(stream)
                        return self.data
                    except yaml.YAMLError as exc:
                        print(exc)
                        return dict()
        return dict()

    def set_config(self, data):
        with open(self.path, 'w', encoding='utf8') as outfile:
            yaml.dump(data, outfile, default_flow_style=False, allow_unicode=True)


if __name__ == "__main__":
    con = SystemConfig()
    print(os.getcwd())

