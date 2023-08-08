from pathlib import Path
from filelock import Timeout, FileLock
import doy.data as data

_kvstore_path = Path("~/.doy_kvstore.json").expanduser()
lock = FileLock(str(_kvstore_path) + ".lock")


@lock
def get_store() -> dict:
    return data.load(_kvstore_path, default={})


@lock
def set_store(store: dict):
    data.dump(store, _kvstore_path)


@lock
def get(key):
    store = get_store()
    return store[key]


@lock
def set(key, value):
    store = get_store()
    store[key] = value
    set_store(store)
