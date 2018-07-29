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

    def win_rate(self, match_ups, teammates):
        theirs_score, ours_score, wr, table = self.bp.win_rate(
            match_ups, teammates, lang=self.lang)
        msg = '胜率:{0:.2f},易发挥:'.format(wr)
        h_list = []
        for i in range(3):
            h_list.append(self.get_abbrev_name(table[i][0]))
        msg += ','.join(h_list)
        print(msg)
        pyperclip.copy(';'.join(msg))


def main():
    o = CNOutput()
    match_ups = [
        CNAbbrevHeroes.冰女
    ]
    teammates = [
        CNAbbrevHeroes.敌法
    ]
    o.recommend(match_ups, teammates)
    team_1 = [CNAbbrevHeroes.巫医,
              CNAbbrevHeroes.克林克兹,
              CNAbbrevHeroes.不朽尸王,
              CNAbbrevHeroes.嗜血狂魔,
              CNAbbrevHeroes.瘟疫法师]
    team_2 = [CNAbbrevHeroes.宙斯,
              CNAbbrevHeroes.全能骑士,
              CNAbbrevHeroes.树精卫士,
              CNAbbrevHeroes.邪影芳灵,
              CNAbbrevHeroes.虚空假面]
    o.win_rate(team_1, team_2)


if __name__ == '__main__':
    main()
