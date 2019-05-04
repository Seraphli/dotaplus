from dpapi.util.util import get_path
import codecs
import json


def load_custom_config():
    with codecs.open(get_path('data/custom', parent=True) +
                     '/custom_config.json') as f:
        return json.load(f)


__all__ = ['load_custom_config']
