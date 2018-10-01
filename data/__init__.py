import codecs
import json
from util.util import get_path

with codecs.open(get_path('data', parent=True) + '/custom_data.json',
                 encoding='utf8') as f:
    CUSTOM_DATA = json.load(f)

with codecs.open(get_path('data', parent=True) + '/complete_custom_data.json',
                 encoding='utf8') as f:
    COMPLETE_CUSTOM_DATA = json.load(f)
