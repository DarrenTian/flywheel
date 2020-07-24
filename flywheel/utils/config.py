import os
from typing import List


class Config(object):
    prefix = 'FW'

    @classmethod
    def get(cls, name, default='') -> str:
        return os.environ.get(f'{cls.prefix}_{name}', default=default)

    @classmethod
    def get_int(cls, name, default=0) -> int:
        return int(cls.get(name, default=str(default)))
    
    @classmethod
    def get_bool(cls, name, default=False) -> bool:
        config = cls.get(name, default=str(default))
        if config != '':
            return 'True' == config
        else:
            return default

    @classmethod
    def get_list(cls, name, default=[]) -> List[str]:
        config = cls.get(name)
        if config != '':
            return config.split(',')
        else:
            return default

    @classmethod
    def get_int_list(cls, name, default=[]) -> List[int]:
        config = cls.get_list(name, default=default)
        return [int(c) for c in config]
