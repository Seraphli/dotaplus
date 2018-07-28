from ban_pick import BanPick
from cfg import Language
from heroes import Heroes, CNHeroes
import pyperclip


class CNOutput(object):
    def __init__(self):
        self.lang = Language.CN
        self.name_key = 'cn_name'
        self.bp = BanPick()

    def recommend(self, match_ups, teammates):
        _h_v = self.bp.cal_match(match_ups, teammates)
        exclude = []
        exclude.extend(match_ups)
        exclude.extend(teammates)
        v_list = self.bp.get_v_list(exclude, _h_v)
        msgs = []
        msg = '推荐:'
        h_list = []
        for i in range(15):
            h_list.append(self.bp.data[v_list[i][0]][self.name_key])
        msg += ','.join(h_list)
        msgs.append(msg)
        print(msg)
        msg = '不推荐:'
        h_list = []
        for i in range(15):
            h_list.append(self.bp.data[v_list[-i - 1][0]][self.name_key])
        msg += ','.join(h_list)
        msgs.append(msg)
        print(msg)
        pyperclip.copy(';'.join(msgs))


def main():
    o = CNOutput()
    o.recommend([], [])


if __name__ == '__main__':
    main()
