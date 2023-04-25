import os
import typing
from collections import defaultdict


def get_latest_file(path: str, name_start: str):
    filename = sorted(x for x in os.listdir(path) if x.startswith(name_start))[-1]

    return os.path.join(path, filename)


class FixedKeyDict(dict):
    def __init__(self, *keys: typing.Hashable, default_value=""):
        super().__init__()
        for key in keys:
            super().__setitem__(key, default_value)

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            raise KeyError(f"Invalid key '{key}'. Set key when creating FixedKeyDict.")

    def __setitem__(self, key, val):
        if key not in self.keys():
            raise KeyError(f"Invalid key '{key}'. Set key when creating FixedKeyDict.")

        super().__setitem__(key, val)
