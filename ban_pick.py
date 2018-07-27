from tabulate import tabulate
import json
import numpy as np
import copy
from heroes import Heroes, CNHeroes


class Language(object):
    EN = 'en'
    CN = 'cn'


class BanPick(object):
    def __init__(self):
        with open('data.json', 'r') as f:
            self.data = json.load(f)

        self.num_heroes = len(self.data.keys())
        self.factor = np.arange(self.num_heroes, 0, -1)
        self.factor = -np.log(self.factor / np.sum(self.factor))
        self.h_v = {}
        for h in self.data:
            self.h_v[h] = 0

    def print_heroes(self, lang=Language.EN):
        if lang == Language.CN:
            name_key = 'cn_name'
        else:
            name_key = 'name'
        print('Heroes List')
        table = []
        for h in self.data:
            table.append([self.data[h][name_key]])
        self.print_table(table, ['Name'])

    def print_table(self, table, headers, floatfmt='.2f'):
        print(tabulate(table, headers=headers, tablefmt='psql',
                       floatfmt=floatfmt, showindex='always'))

    def apply_factor(self, h_v, sorted_list, f=1.0):
        h_v = copy.deepcopy(h_v)
        for idx, _h in enumerate(sorted_list):
            _h = _h[0]
            h_v[_h] += f * self.factor[idx]
        return h_v

    def print_v_list(self, n=15, exclude=None, h_v=None, lang=Language.EN):
        if lang == Language.CN:
            name_key = 'cn_name'
        else:
            name_key = 'name'
        if h_v is None:
            h_v = self.h_v
        if exclude:
            _num = self.num_heroes - len(exclude)
        else:
            _num = self.num_heroes
        v_list = []
        for _h, _v in h_v.items():
            if exclude and _h in exclude:
                continue
            v_list.append([_h, _v])
        v_list = sorted(v_list, key=lambda x: x[1], reverse=True)
        print('Recommended')
        table = []
        for i in range(n):
            table.append([self.data[v_list[i][0]][name_key], v_list[i][1]])
        self.print_table(table, ['Name', 'Value'])
        print('Not Recommended')
        table = []
        for i in range(n):
            table.append([self.data[v_list[_num - i - 1][0]][name_key],
                          v_list[_num - i - 1][1]])
        self.print_table(table, ['Name', 'Value'])

    def pre_calculated(self, lang=Language.EN):
        h_wr = []
        for h in self.data:
            h_wr.append([h, self.data[h]['win_rate']])
        h_wr = sorted(h_wr, key=lambda x: x[1])
        self.h_v = self.apply_factor(self.h_v, h_wr, 0.5)

        h_mu = []
        h_mu_dict = {}
        for h in self.data:
            total_pos = 0
            total_neg = 0
            for mu in self.data[h]['match_ups']:
                anti_index = self.data[h]['match_ups'][mu]
                if anti_index > 0:
                    total_pos += anti_index
                else:
                    total_neg += anti_index
                if mu not in h_mu_dict:
                    h_mu_dict[mu] = 0
                h_mu_dict[mu] += -anti_index
            h_mu.append([h, total_pos, total_neg])
        h_mu_pos = sorted(h_mu, key=lambda x: x[1])
        self.h_v = self.apply_factor(self.h_v, h_mu_pos, 0.3)
        h_mu_neg = sorted(h_mu, key=lambda x: x[2])
        self.h_v = self.apply_factor(self.h_v, h_mu_neg, 0.3)
        h_mu = []
        for h in h_mu_dict:
            h_mu.append([h, h_mu_dict[h]])
        h_mu = sorted(h_mu, key=lambda x: x[1])
        self.h_v = self.apply_factor(self.h_v, h_mu, 0.3)

        h_tm = []
        h_tm_dict = {}
        for h in self.data:
            total_pos = 0
            total_neg = 0
            for tm in self.data[h]['teammates']:
                coop_index = self.data[h]['teammates'][tm]
                if coop_index > 0:
                    total_pos += coop_index
                else:
                    total_neg += coop_index
                if tm not in h_tm_dict:
                    h_tm_dict[tm] = 0
                h_tm_dict[tm] += coop_index
            h_tm.append([h, total_pos, total_neg])
        h_tm_pos = sorted(h_tm, key=lambda x: x[1])
        self.h_v = self.apply_factor(self.h_v, h_tm_pos, 0.3)
        h_tm_neg = sorted(h_tm, key=lambda x: (x[2], x[1]))
        self.h_v = self.apply_factor(self.h_v, h_tm_neg, 0.3)
        h_tm = []
        for h in h_tm_dict:
            h_tm.append([h, h_tm_dict[h]])
        h_tm = sorted(h_tm, key=lambda x: x[1])
        self.h_v = self.apply_factor(self.h_v, h_tm, 0.3)

        self.print_v_list(lang=lang)

    def cal_match(self, match_ups, teammates):
        _h_v = copy.deepcopy(self.h_v)
        for mu in match_ups:
            mu_index = []
            for _mu in self.data[mu]['match_ups']:
                mu_index.append([_mu, -self.data[mu]['match_ups'][_mu]])
            mu_index = sorted(mu_index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, mu_index, 1.0)

            mu_index = []
            for h in self.data:
                if h == mu:
                    continue
                mu_index.append([h, self.data[h]['match_ups'][mu]])
            mu_index = sorted(mu_index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, mu_index, 1.0)

        for tm in teammates:
            tm_index = []
            for _tm in self.data[tm]['teammates']:
                tm_index.append([_tm, self.data[tm]['match_ups'][_tm]])
            tm_index = sorted(tm_index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, tm_index, 0.8)
        return _h_v

    def recommend(self, match_ups, teammates, lang=Language.EN):
        _h_v = self.cal_match(match_ups, teammates)
        exclude = []
        exclude.extend(match_ups)
        exclude.extend(teammates)
        self.print_v_list(exclude=exclude, h_v=_h_v, lang=lang)

    def win_rate(self, match_ups, teammates, lang=Language.EN):
        if lang == Language.CN:
            name_key = 'cn_name'
            wr_text = '胜率'
        else:
            name_key = 'name'
            wr_text = 'Win rate'
        _h_v = self.cal_match(match_ups, teammates)
        table = []
        theirs_score = []
        for mu in match_ups:
            theirs_score.append(_h_v[mu])
            table.append([self.data[mu][name_key], _h_v[mu]])
        _theirs_score = sum(theirs_score) / len(theirs_score)
        ours_score = []
        for tm in teammates:
            ours_score.append(_h_v[tm])
            table.append([self.data[tm][name_key], _h_v[tm]])
        _ours_score = sum(ours_score) / len(ours_score)
        wr = _ours_score / (_ours_score + _theirs_score)
        table.append([wr_text, wr])
        self.print_table(table, headers=['Name', 'Value'], floatfmt='.4f')
        return theirs_score, ours_score, wr


def main():
    lang = Language.CN
    bp = BanPick()
    bp.print_heroes(lang=lang)
    bp.pre_calculated(lang=lang)
    bp.recommend([Heroes.Crystal_Maiden,
                  Heroes.Lina,
                  Heroes.Bloodseeker,
                  Heroes.Batrider,
                  Heroes.Nyx_Assassin],
                 [Heroes.Troll_Warlord,
                  Heroes.Natures_Prophet,
                  Heroes.Lich,
                  Heroes.Slardar], lang=Language.EN)
    bp.recommend([CNHeroes.水晶室女,
                  CNHeroes.莉娜,
                  CNHeroes.嗜血狂魔,
                  CNHeroes.蝙蝠骑士,
                  CNHeroes.司夜刺客],
                 [CNHeroes.巨魔战将,
                  CNHeroes.先知,
                  CNHeroes.巫妖,
                  CNHeroes.斯拉达], lang=lang)
    bp.win_rate([CNHeroes.水晶室女,
                 CNHeroes.莉娜,
                 CNHeroes.嗜血狂魔,
                 CNHeroes.蝙蝠骑士,
                 CNHeroes.司夜刺客],
                [CNHeroes.巨魔战将,
                 CNHeroes.先知,
                 CNHeroes.巫妖,
                 CNHeroes.斯拉达,
                 CNHeroes.噬魂鬼], lang=lang)
    bp.win_rate([CNHeroes.末日使者,
                 CNHeroes.主宰,
                 CNHeroes.沉默术士,
                 CNHeroes.水晶室女,
                 CNHeroes.炼金术士],
                [CNHeroes.冥魂大帝,
                 CNHeroes.莱恩,
                 CNHeroes.钢背兽,
                 CNHeroes.斯拉达,
                 CNHeroes.宙斯], lang=lang)


if __name__ == '__main__':
    main()
