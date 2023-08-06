import os

from . import util
import json


class JsonConf:
    __root_path: str
    __platform: str
    __config: {}

    def __init__(self, location):
        self.__root_path = os.path.join(util.user_location_get(), location)
        self.__config = self.config_get()

    def put_item(self, key: str, value: str):
        self.__config.__setitem__(key, value)
        fo = open(self.__root_path, "w+", encoding='utf8')
        json.dump(self.__config, fo)
        fo.close()

    def put_dir(self, obj: dict):
        for k in obj.keys():
            self.__config.__setitem__(k, obj.get(k))
        fo = open(self.__root_path, "w+", encoding='utf8')
        json.dump(self.__config, fo)
        fo.close()

    def config(self):
        return self.__config

    def config_get(self):
        config = {}
        try:
            os.makedirs(os.path.dirname(self.__root_path))
        except OSError:
            pass
        try:
            fo = open(self.__root_path, "r", encoding='utf8')
            config = json.loads(fo.read())
            fo.close()
        except FileNotFoundError:
            pass
        return config
