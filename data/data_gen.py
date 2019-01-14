import codecs
import json
from data import CUSTOM_DATA
import copy


class DataGen(object):
    @staticmethod
    def judge_pure_english(keyword):
        return all(ord(c) < 128 for c in keyword)

    @staticmethod
    def get_cn_abbrev_name(hero):
        names = CUSTOM_DATA['abbrev_dict'][hero]
        min_len = 10
        abbrev = ''
        for name in names:
            if min_len > len(name):
                abbrev = name
                min_len = len(name)
            elif min_len == len(name) and ord(name[0]) > 255:
                abbrev = name
                min_len = len(name)
        return abbrev

    @staticmethod
    def gen_complete_custom_data():
        from dpapi.util.util import get_path
        c_data = copy.deepcopy(CUSTOM_DATA)
        with codecs.open(get_path('data', parent=True) +
                         '/data.json', encoding='utf8') as f:
            web_data = json.load(f)
        # Generate english layout
        heroes = c_data['cn_layout']
        str_hero_num = sum(c_data['main_interface_hero']['num'][0])
        agi_hero_num = sum(c_data['main_interface_hero']['num'][1])
        int_hero_num = sum(c_data['main_interface_hero']['num'][2])
        str_heroes = copy.deepcopy(heroes[:str_hero_num])
        agi_heroes = copy.deepcopy(heroes[str_hero_num:str_hero_num +
                                                       agi_hero_num])
        int_heroes = copy.deepcopy(heroes[-int_hero_num:])
        str_heroes = [[h, web_data[h]['name']] for h in str_heroes]
        agi_heroes = [[h, web_data[h]['name']] for h in agi_heroes]
        int_heroes = [[h, web_data[h]['name']] for h in int_heroes]
        str_heroes = [h for h, name in sorted(str_heroes, key=lambda x: x[1])]
        agi_heroes = [h for h, name in sorted(agi_heroes, key=lambda x: x[1])]
        int_heroes = [h for h, name in sorted(int_heroes, key=lambda x: x[1])]
        c_data['en_layout'] = copy.deepcopy(str_heroes)
        c_data['en_layout'].extend(agi_heroes)
        c_data['en_layout'].extend(int_heroes)
        c_data['cn_short_abbrev'] = {}
        c_data['inverse_abbrev_dict'] = {}
        for h in web_data:
            abbrev = c_data['abbrev_dict'][h]

            name = web_data[h]['name']
            low = []
            for _abbrev in abbrev:
                if DataGen.judge_pure_english(_abbrev):
                    low.append(_abbrev.lower())
            abbrev = [name, name.lower()] + low + abbrev
            abbrev = sorted(set(abbrev), key=abbrev.index)
            for a in abbrev:
                c_data['inverse_abbrev_dict'][a] = h
            c_data['abbrev_dict'][h] = abbrev
            c_data['cn_short_abbrev'][h] = DataGen.get_cn_abbrev_name(h)

        path = get_path('data', parent=True) + '/complete_custom_data.json'
        with codecs.open(path, 'w', encoding='utf8')as f:
            json.dump(c_data, f)


if __name__ == '__main__':
    DataGen.gen_complete_custom_data()
