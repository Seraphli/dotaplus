import codecs
from data.cfg import Interface
from urllib.request import urlretrieve
import json
from util import get_path

with codecs.open('custom_data.json', encoding='utf8') as f:
    custom_data = json.load(f)

CN_ABBREV_DICT = custom_data['CN_ABBREV_DICT']
CN_LAYOUT = custom_data['CN_LAYOUT']


def get_hero(name):
    for k, v in CN_ABBREV_DICT.items():
        if name.upper() == k.upper() or name.upper() in v:
            return k

    raise ValueError('Cannot find hero: {}'.format(name))


def to_key_name(heroes):
    heroes = [get_hero(name) for name in heroes]
    return heroes


def generate_abbrev_name_py():
    lines = ['class CNAbbrevHeroes(object):\n'
             '    none = "none"\n'
             '    无 = "none"\n']
    for h in CN_ABBREV_DICT:
        lines.append('    {} = "{}"\n'.format(h, h))
        for abbrev in CN_ABBREV_DICT[h]:
            if ord(abbrev[0]) < 255:
                lines.append('    {} = "{}"\n'.format(abbrev.upper(), h))
                lines.append('    {} = "{}"\n'.format(abbrev.lower(), h))
            else:
                lines.append('    {} = "{}"\n'.format(abbrev, h))
    with codecs.open('cn_heroes.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)


def generate_hero_index_py():
    head = 'HERO_INDEX = {\n'
    tail = '\n}\n'
    _lines = []
    hero_num = Interface.HERO_NUM
    counter = 0
    for c, rows in enumerate(hero_num):
        for row, col_n in enumerate(rows):
            for col in range(col_n):
                _lines.append('    "{}": "{}"'.format((c, row, col),
                                                      CN_LAYOUT[counter]))
                counter += 1
    content = head + ',\n'.join(_lines) + tail
    with codecs.open('hero_index.py', 'w', encoding='utf-8') as f:
        f.write(content)


def get_heroes_image():
    image_url = 'http://media.steampowered.com/apps/' \
                'dota2/images/heroes/{}_lg.png'
    with open('data.json') as f:
        data = json.load(f)
    for h in data:
        url = image_url.format(h)
        urlretrieve(url, get_path('res/heroes') +
                    '/{}.png'.format(h))


def main():
    generate_abbrev_name_py()
    generate_hero_index_py()
    get_heroes_image()


if __name__ == '__main__':
    main()
