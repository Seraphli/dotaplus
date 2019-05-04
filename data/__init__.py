import codecs
import json
from dpapi.util.util import get_path

with codecs.open(get_path('data/custom', parent=True) + '/custom_data.json',
                 encoding='utf8') as f:
    CUSTOM_DATA = json.load(f)

with codecs.open(
        get_path('data/custom', parent=True) + '/complete_custom_data.json',
        encoding='utf8') as f:
    COMPLETE_CUSTOM_DATA = json.load(f)
