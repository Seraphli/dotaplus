from tabulate import tabulate
import json
import numpy as np
import copy
from cn_heroes import CNAbbrevHeroes
from cfg import Language, MainHeroInterface
from reason import Reasons, get_good_reason, get_bad_reason


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
        self.reason_n = 10

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

    def get_v_list(self, h_v, available=None, exclude=None):
        v_list = []
        for _h, _v in h_v.items():
            if exclude and _h in exclude:
                continue
            if available:
                if _h in available:
                    v_list.append([_h, _v])
            else:
                v_list.append([_h, _v])
        v_list = sorted(v_list, key=lambda x: x[1], reverse=True)
        return v_list

    def get_recommend(self, v_list, reasons, n=15):
        table_1 = []
        for i in range(n):
            h = v_list[i][0]
            table_1.append([v_list[i][0], v_list[i][1],
                            get_good_reason(h, reasons)])
        table_2 = []
        for i in range(n):
            h = v_list[-i - 1][0]
            table_2.append([v_list[-i - 1][0], v_list[-i - 1][1],
                            get_bad_reason(h, reasons)])
        return table_1, table_2

    def convert_table_lang(self, table, lang=Language.EN):
        if lang == Language.CN:
            name_key = 'cn_name'
        else:
            name_key = 'name'
        _table = []
        for i in table:
            if i[0] not in self.data:
                _table.append(i)
                continue
            reason = i[2]
            for h in self.data:
                if h in reason:
                    reason = reason.replace(h, self.data[h][name_key])
            _table.append([self.data[i[0]][name_key], i[1], reason])
        return _table

    def print_recommend(self, table_1, table_2):
        print('Recommend')
        self.print_table(table_1, ['Name', 'Value', 'Reason'])
        self.print_table(table_2, ['Name', 'Value', 'Reason'])

    def pre_calculated(self, h_v, reasons, factor=1.0):
        h_v = copy.deepcopy(h_v)
        reasons = copy.deepcopy(reasons)
        # Based on win rate
        h_wr = []
        for h in self.data:
            h_wr.append([h, self.data[h]['win_rate']])
        h_wr = sorted(h_wr, key=lambda x: x[1])
        h_v = self.apply_factor(h_v, h_wr, 0.5 * factor)
        reasons[Reasons.N_WIN_RATE] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_WIN_RATE].append(h_wr[i][0])
        reasons[Reasons.WIN_RATE] = []
        for i in range(self.reason_n):
            reasons[Reasons.WIN_RATE].append(h_wr[-i - 1][0])

        # Based on match up index
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
        h_v = self.apply_factor(h_v, h_mu_pos, 0.5 * factor)
        reasons[Reasons.N_ANTI_INDEX_POS] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_ANTI_INDEX_POS].append(h_mu_pos[i][0])
        reasons[Reasons.ANTI_INDEX_POS] = []
        for i in range(self.reason_n):
            reasons[Reasons.ANTI_INDEX_POS].append(h_mu_pos[-i - 1][0])
        h_mu_neg = sorted(h_mu, key=lambda x: x[2])
        h_v = self.apply_factor(h_v, h_mu_neg, 0.5 * factor)
        reasons[Reasons.N_ANTI_INDEX_NEG] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_ANTI_INDEX_NEG].append(h_mu_neg[i][0])
        reasons[Reasons.ANTI_INDEX_NEG] = []
        for i in range(self.reason_n):
            reasons[Reasons.ANTI_INDEX_NEG].append(h_mu_neg[-i - 1][0])
        h_mu = []
        for h in h_mu_dict:
            h_mu.append([h, h_mu_dict[h]])
        h_mu = sorted(h_mu, key=lambda x: x[1])
        h_v = self.apply_factor(h_v, h_mu, 0.5 * factor)
        reasons[Reasons.N_ANTI_INDEX] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_ANTI_INDEX].append(h_mu[i][0])
        reasons[Reasons.ANTI_INDEX] = []
        for i in range(self.reason_n):
            reasons[Reasons.ANTI_INDEX].append(h_mu[-i - 1][0])

        # Based on teammate index
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
        h_v = self.apply_factor(h_v, h_tm_pos, 0.5 * factor)
        reasons[Reasons.N_COOP_INDEX_POS] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_COOP_INDEX_POS].append(h_tm_pos[i][0])
        reasons[Reasons.COOP_INDEX_POS] = []
        for i in range(self.reason_n):
            reasons[Reasons.COOP_INDEX_POS].append(h_tm_pos[-i - 1][0])
        h_tm_neg = sorted(h_tm, key=lambda x: (x[2], x[1]))
        h_v = self.apply_factor(h_v, h_tm_neg, 0.5 * factor)
        reasons[Reasons.N_COOP_INDEX_NEG] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_COOP_INDEX_NEG].append(h_tm_neg[i][0])
        reasons[Reasons.COOP_INDEX_NEG] = []
        for i in range(self.reason_n):
            reasons[Reasons.COOP_INDEX_NEG].append(h_tm_neg[-i - 1][0])
        h_tm = []
        for h in h_tm_dict:
            h_tm.append([h, h_tm_dict[h]])
        h_tm = sorted(h_tm, key=lambda x: x[1])
        h_v = self.apply_factor(h_v, h_tm, 0.5 * factor)
        reasons[Reasons.N_COOP_INDEX] = []
        for i in range(self.reason_n):
            reasons[Reasons.N_COOP_INDEX].append(h_tm[i][0])
        reasons[Reasons.COOP_INDEX] = []
        for i in range(self.reason_n):
            reasons[Reasons.COOP_INDEX].append(h_tm[-i - 1][0])
        return h_v, reasons

    def cal_match(self, h_v, reasons, match_ups, teammates):
        _h_v = copy.deepcopy(h_v)
        reasons = copy.deepcopy(reasons)
        reasons[Reasons.N_MATCH_UPS] = {}
        reasons[Reasons.MATCH_UPS] = {}
        reasons[Reasons.N_TEAMMATES] = {}
        reasons[Reasons.TEAMMATES] = {}
        for mu in match_ups:
            mu_index = []
            for _mu in self.data[mu]['match_ups']:
                mu_index.append([_mu, -self.data[mu]['match_ups'][_mu]])
            mu_index = sorted(mu_index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, mu_index, 1.0)
            for i in range(self.reason_n):
                if mu_index[i][0] not in reasons[Reasons.N_MATCH_UPS]:
                    reasons[Reasons.N_MATCH_UPS][mu_index[i][0]] = []
                if mu not in reasons[Reasons.N_MATCH_UPS][mu_index[i][0]]:
                    reasons[Reasons.N_MATCH_UPS][mu_index[i][0]].append(mu)
            for i in range(self.reason_n):
                if mu_index[-i - 1][0] not in reasons[Reasons.MATCH_UPS]:
                    reasons[Reasons.MATCH_UPS][mu_index[-i - 1][0]] = []
                if mu not in reasons[Reasons.MATCH_UPS][mu_index[-i - 1][0]]:
                    reasons[Reasons.MATCH_UPS][mu_index[-i - 1][0]].append(mu)

            mu_index = []
            for h in self.data:
                if h == mu:
                    continue
                mu_index.append([h, self.data[h]['match_ups'][mu]])
            mu_index = sorted(mu_index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, mu_index, 1.0)
            for i in range(self.reason_n):
                if mu_index[i][0] not in reasons[Reasons.N_MATCH_UPS]:
                    reasons[Reasons.N_MATCH_UPS][mu_index[i][0]] = []
                if mu not in reasons[Reasons.N_MATCH_UPS][mu_index[i][0]]:
                    reasons[Reasons.N_MATCH_UPS][mu_index[i][0]].append(mu)
            for i in range(self.reason_n):
                if mu_index[-i - 1][0] not in reasons[Reasons.MATCH_UPS]:
                    reasons[Reasons.MATCH_UPS][mu_index[-i - 1][0]] = []
                if mu not in reasons[Reasons.MATCH_UPS][mu_index[-i - 1][0]]:
                    reasons[Reasons.MATCH_UPS][mu_index[-i - 1][0]].append(mu)

        for tm in teammates:
            tm_index = []
            for _tm in self.data[tm]['teammates']:
                tm_index.append([_tm, self.data[tm]['match_ups'][_tm]])
            tm_index = sorted(tm_index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, tm_index, 0.8)
            for i in range(self.reason_n):
                if tm_index[i][0] not in reasons[Reasons.N_TEAMMATES]:
                    reasons[Reasons.N_TEAMMATES][tm_index[i][0]] = []
                if tm not in reasons[Reasons.N_TEAMMATES][tm_index[i][0]]:
                    reasons[Reasons.N_TEAMMATES][tm_index[i][0]].append(tm)
            for i in range(self.reason_n):
                if tm_index[-i - 1][0] not in reasons[Reasons.TEAMMATES]:
                    reasons[Reasons.TEAMMATES][tm_index[-i - 1][0]] = []
                if tm not in reasons[Reasons.TEAMMATES][tm_index[-i - 1][0]]:
                    reasons[Reasons.TEAMMATES][tm_index[-i - 1][0]].append(tm)

        if len(teammates) > 0:
            team_role = {}
            for role in MainHeroInterface.ROLE_NAME.values():
                team_role[role] = 0
            for tm in teammates:
                for role in MainHeroInterface.ROLE_NAME.values():
                    team_role[role] += self.data[tm]['role'][role]
            _role = copy.deepcopy(team_role)
            min_role = min(_role, key=team_role.get)
            max_role = max(_role, key=team_role.get)
            index = []
            for h in self.data:
                value = self.data[h]['role'][min_role]
                value += -self.data[h]['role'][max_role]
                index.append([h, value])
            index = sorted(index, key=lambda x: x[1])
            _h_v = self.apply_factor(_h_v, index, 1)
            if team_role['Carry'] >= 4:
                index = []
                for h in self.data:
                    value = -self.data[h]['role']['Carry']
                    index.append([h, value])
                index = sorted(index, key=lambda x: x[1])
                _h_v = self.apply_factor(_h_v, index, 1)
            if team_role['Support'] >= 5:
                index = []
                for h in self.data:
                    value = -self.data[h]['role']['Support']
                    index.append([h, value])
                index = sorted(index, key=lambda x: x[1])
                _h_v = self.apply_factor(_h_v, index, 1)

        return _h_v, reasons

    def recommend(self, match_ups, teammates, available=None):
        if len(match_ups) == 5 and len(teammates) == 5:
            return
        exclude = []
        exclude.extend(match_ups)
        exclude.extend(teammates)
        if len(exclude) == 0:
            factor = 1.0
        else:
            factor = min(1.0, len(exclude) * 0.2)
        reasons = {}
        _h_v, reasons = self.pre_calculated(self.h_v, reasons, factor)
        _h_v, reasons = self.cal_match(_h_v, reasons, match_ups, teammates)
        v_list = self.get_v_list(_h_v, available=available, exclude=exclude)
        table_1, table_2 = self.get_recommend(v_list, reasons)
        return _h_v, reasons, v_list, table_1, table_2

    def win_rate(self, match_ups, teammates, lang=Language.EN):
        if len(match_ups) != 5 or len(teammates) != 5:
            return
        if lang == Language.CN:
            wr_text = '胜率'
        else:
            wr_text = 'Win rate'
        reasons = {}
        _h_v, reasons = self.pre_calculated(self.h_v, reasons)
        _h_v_1, reasons_1 = self.cal_match(_h_v, reasons, match_ups, teammates)
        _h_v_2, reasons_2 = self.cal_match(_h_v, reasons, teammates, match_ups)
        table = []
        ours_score = []
        for tm in teammates:
            ours_score.append(_h_v_1[tm])
            table.append([tm, _h_v_1[tm],
                          get_good_reason(tm, reasons_1)])
        theirs_score = []
        for mu in match_ups:
            theirs_score.append(_h_v_2[mu])
            table.append([mu, _h_v_2[mu],
                          get_good_reason(mu, reasons_2)])
        _theirs_score = sum(theirs_score) / len(theirs_score)
        table = sorted(table, key=lambda x: x[1], reverse=True)
        _ours_score = sum(ours_score) / len(ours_score)
        wr = _ours_score / (_ours_score + _theirs_score) * 100
        table.append([wr_text, wr, ''])
        return theirs_score, ours_score, wr, table

    def remove_none(self, match_ups, teammates):
        _match_ups = []
        for mu in match_ups:
            if mu == CNAbbrevHeroes.none:
                continue
            _match_ups.append(mu)
        _teammates = []
        for tm in teammates:
            if tm == CNAbbrevHeroes.none:
                continue
            _teammates.append(tm)
        return _match_ups, _teammates


class BanPickGame(object):
    def __init__(self, ban_pick, available, teams, team_no):
        self.bp = ban_pick
        self.available = available
        # remove none before initialize
        self.teams = self.bp.remove_none(*teams)
        self.team_no = team_no

    def get_moves(self):
        if len(self.teams[0]) == 5 and len(self.teams[1]) == 5:
            return []
        return copy.deepcopy(self.available)

    def do_move(self, move):
        self.available.remove(move)
        if len(self.teams[0]) < 5:
            self.teams[0].append(move)
        elif len(self.teams[1]) < 5:
            self.teams[1].append(move)

    def clone(self):
        return BanPickGame(self.bp, copy.deepcopy(self.available),
                           copy.deepcopy(self.teams), self.team_no)

    def is_game_over(self):
        return sum([len(t) for t in self.teams if t != 'none']) == 10

    def get_result(self):
        teammates = self.teams[self.team_no]
        match_ups = self.teams[1 - self.team_no]
        _, _, wr, _ = self.bp.win_rate(match_ups, teammates)
        return wr


def main():
    match_ups = [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none]
    teammates = [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none, CNAbbrevHeroes.none,
                 CNAbbrevHeroes.none]
    lang = Language.CN
    bp = BanPick()
    match_ups, teammates = bp.remove_none(match_ups, teammates)
    r = bp.recommend(match_ups, teammates)
    if r is not None:
        _, _, _, t_1, t_2 = r
        t_1 = bp.convert_table_lang(t_1, lang)
        t_2 = bp.convert_table_lang(t_2, lang)
        bp.print_recommend(t_1, t_2)
    r = bp.win_rate(match_ups, teammates, lang=lang)
    if r is not None:
        _, _, _, table = r
        table = bp.convert_table_lang(table, lang)
        bp.print_table(table, headers=['Name', 'Value', 'Reason'])


if __name__ == '__main__':
    main()
