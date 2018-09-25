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

    def recommend_str(self, match_ups, teammates, available=None):
        if len(match_ups) == 5 and len(teammates) == 5:
            return
        _h_v, reasons, v_list, _, _ = self.bp.recommend(
            match_ups, teammates, available)
        msgs = []
        msg = '推荐:'
        h_list = []
        for i in range(15):
            h = v_list[i][0]
            h_list.append(self.get_abbrev_name(h))
        msg += ','.join(h_list)
        msgs.append(msg)
        msg = '不推荐:'
        h_list = []
        for i in range(15):
            h = v_list[-i - 1][0]
            h_list.append(self.get_abbrev_name(h))
        msg += ','.join(h_list)
        msgs.append(msg)
        return ';'.join(msgs)

    def recommend(self, match_ups, teammates, available=None):
        msg = self.recommend_str(match_ups, teammates, available)
        print(msg)
        pyperclip.copy(msg.split(';')[0])

    def win_rate_str(self, match_ups, teammates):
        if len(match_ups) != 5 or len(teammates) != 5:
            return
        theirs_score, ours_score, wr, table = self.bp.win_rate(
            match_ups, teammates, lang=self.lang)
        msg = '胜率:{0:.2f},易发挥:'.format(wr)
        h_list = []
        for i in range(3):
            h_list.append(self.get_abbrev_name(table[i][0]))
        msg += ','.join(h_list)
        return msg

    def win_rate(self, match_ups, teammates):
        msg = self.win_rate_str(match_ups, teammates)
        print(msg)
        pyperclip.copy(msg)


def main():
    match_ups = [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none]
    teammates = [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none]
    o = CNOutput()
    match_ups, teammates = o.bp.remove_none(match_ups, teammates)
    o.recommend(match_ups, teammates)
    team_1 = match_ups
    team_2 = teammates
    o.win_rate(team_1, team_2)


if __name__ == '__main__':
    main()
