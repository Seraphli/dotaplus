from ban_pick import BanPick
from cfg import Language
from cn_heroes import CNAbbrevHeroes
import pyperclip
from custom_data import CN_ABBREV_DICT


class CNOutput(object):
    def __init__(self):
        self.lang = Language.CN
        self.name_key = 'cn_name'
        self.bp = BanPick()

    def get_abbrev_name(self, hero):
        names = CN_ABBREV_DICT[hero]
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

    def recommend(self, match_ups, teammates):
        _h_v, reasons, v_list, _, _ = self.bp.recommend(match_ups, teammates)
        msgs = []
        msg = '推荐:'
        h_list = []
        for i in range(15):
            h = v_list[i][0]
            h_list.append(self.get_abbrev_name(h))
        msg += ','.join(h_list)
        msgs.append(msg)
        print(msg)
        msg = '不推荐:'
        h_list = []
        for i in range(15):
            h = v_list[-i - 1][0]
            h_list.append(self.get_abbrev_name(h))
        msg += ','.join(h_list)
        msgs.append(msg)
        print(msg)
        pyperclip.copy(';'.join(msgs))


def main():
    o = CNOutput()
    match_ups = [
        CNAbbrevHeroes.冰女
    ]
    teammates = [
        CNAbbrevHeroes.敌法
    ]
    o.recommend(match_ups, teammates)


if __name__ == '__main__':
    main()
