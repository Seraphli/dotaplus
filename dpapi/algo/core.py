import numpy as np
import copy
from dpapi.algo.reason import Reasons, CN_REASON_DICT
from dpapi.util.cfg import load_custom_config
from dpapi.util.util import get_path
import json
import codecs

REASON_N = 10


class Core(object):
    def __init__(self):
        self.web_data = {}
        self.database = {}

        data_path = get_path('data/generated', parent=True) + '/name_dict.json'
        with codecs.open(data_path, encoding='utf-8') as f:
            self.name_dict = json.load(f)

        num_heroes = len(self.name_dict.keys())
        self.weight = np.arange(num_heroes, 0, -1)
        self.weight = -np.log(self.weight / np.sum(self.weight))

    def load_data(self):
        data_path = get_path('data/server', parent=True) + '/web_data.json'
        with codecs.open(data_path, encoding='utf-8') as f:
            self.web_data = json.load(f)

        self.database = {}
        dotamax_cfg = load_custom_config()['Dotamax']
        for server in dotamax_cfg['Server']:
            for skill in dotamax_cfg['Skill']:
                for ladder in dotamax_cfg['Ladder']:
                    config_str = '_'.join([server, skill, ladder])
                    hero_value, reasons = self.calculate_based_on_cfg(
                        config_str)
                    self.database[config_str] = {
                        'hero_value': hero_value,
                        'reasons': reasons
                    }
        print('Load data complete')

    def get_data(self, config_str):
        data = self.database[config_str]
        hero_value, reasons = data['hero_value'], data['reasons']
        return copy.deepcopy(hero_value), copy.deepcopy(reasons)

    def init_value(self):
        hero_value = {}
        for h in self.web_data:
            hero_value[h] = 0
        reasons = {}
        return hero_value, reasons

    def add_weight(self, hero_value, sorted_list, factor=1.0):
        hero_value = copy.deepcopy(hero_value)
        for idx, _h in enumerate(sorted_list):
            _h = _h[0]
            hero_value[_h] += factor * self.weight[idx]
        return hero_value

    def add_weight_by_set(self, hero_value, sorted_list, factor=1.0):
        hero_value = copy.deepcopy(hero_value)
        v_list = [v for h, v in sorted_list]
        v_list = sorted(set(v_list), key=v_list.index)
        interval = len(self.weight) / (len(v_list) - 1)
        for hero, value in sorted_list:
            hero_value[hero] += factor * self.weight[
                min(int(v_list.index(value) * interval), len(sorted_list) - 1)]
        return hero_value

    @staticmethod
    def apply_factor(hero_value, factor):
        hero_value = copy.deepcopy(hero_value)
        for hero in hero_value:
            hero_value[hero] *= factor
        return hero_value

    @staticmethod
    def remove_none(match_ups, teammates):
        _match_ups = []
        for mu in match_ups:
            if mu == 'none':
                continue
            _match_ups.append(mu)
        _teammates = []
        for tm in teammates:
            if tm == 'none':
                continue
            _teammates.append(tm)
        return _match_ups, _teammates

    @staticmethod
    def get_v_list(hero_value, available):
        sorted_list = []
        for hero, value in hero_value.items():
            if hero in available:
                sorted_list.append([hero, value])
        sorted_list = sorted(sorted_list, key=lambda x: x[1], reverse=True)
        return sorted_list

    @staticmethod
    def collect_reason(reasons, reason, sorted_list):
        reasons['-' + reason] = []
        for i in range(REASON_N):
            reasons['-' + reason].append(sorted_list[i][0])
        reasons[reason] = []
        for i in range(REASON_N):
            reasons[reason].append(sorted_list[-i - 1][0])

    @staticmethod
    def collect_match_reason(reasons, reason, sorted_list, hero):
        for i in range(REASON_N):
            other = sorted_list[i][0]
            if other not in reasons['-' + reason]:
                reasons['-' + reason][other] = []
            if hero not in reasons['-' + reason][other]:
                reasons['-' + reason][other].append(hero)
        for i in range(REASON_N):
            other = sorted_list[-i - 1][0]
            if other not in reasons[reason]:
                reasons[reason][other] = []
            if hero not in reasons[reason][other]:
                reasons[reason][other].append(hero)

    def calculate(self, cfg, match_ups, teammates, available):
        config_str = cfg['config_str']
        if len(match_ups) == 5 and len(teammates) == 5:
            return self.win_rate(config_str, match_ups, teammates)
        else:
            roles = cfg['roles']
            return self.recommend(config_str, match_ups, teammates,
                                  available, roles)

    def recommend(self, config_str, match_ups, teammates, available, roles):
        heroes = []
        heroes.extend(match_ups)
        heroes.extend(teammates)
        # Adjusting factor
        if len(heroes) == 0:
            factor = 1.0
        else:
            factor = min(1.0, len(heroes) * 0.2)
        hero_value, reasons = self.get_data(config_str)
        self.apply_factor(hero_value, factor)
        hero_value, reasons = self.cal_match(
            config_str, hero_value, reasons, match_ups, teammates)
        hero_value = self.cal_role(hero_value, roles)
        v_list = self.get_v_list(hero_value, available)
        table = self.get_recommend_table(v_list, reasons)
        output = Core.get_cn_recommend_output(v_list)
        return {
            'hero_value': hero_value, 'reasons': reasons,
            'v_list': v_list, 'table': table, 'output': output
        }

    def win_rate(self, config_str, match_ups, teammates):
        hero_value, reasons = self.get_data(config_str)
        ours_hero_value, ours_reasons = self.cal_match(
            config_str, hero_value, reasons, match_ups, teammates)
        theirs_hero_value, theirs_reasons = self.cal_match(
            config_str, hero_value, reasons, teammates, match_ups)
        win_rate, output_table, table, = self.get_win_rate_table(
            match_ups, teammates, ours_hero_value, ours_reasons,
            theirs_hero_value, theirs_reasons)
        output = self.get_cn_win_rate_output(win_rate, table)
        return {
            'ours_hero_value': ours_hero_value,
            'ours_reasons': ours_reasons,
            'theirs_hero_value': theirs_hero_value,
            'theirs_reasons': theirs_reasons,
            'win_rate': win_rate, 'table': output_table, 'output': output
        }

    def get_win_rate_table(self, match_ups, teammates,
                           ours_hero_value, ours_reasons,
                           theirs_hero_value, theirs_reasons):
        table = []
        output_table = []
        ours_score = []
        for idx, hero in enumerate(teammates):
            ours_score.append(ours_hero_value[hero])
            table.append([hero, ours_hero_value[hero], self.get_reason(
                hero, ours_reasons, [Reasons.MATCH_UPS,
                                     Reasons.TEAMMATES],
                lambda r: '-' not in r)])
        theirs_score = []
        for idx, hero in enumerate(match_ups):
            theirs_score.append(theirs_hero_value[hero])
            table.append([hero, ours_hero_value[hero], self.get_reason(
                hero, theirs_reasons, [Reasons.MATCH_UPS,
                                       Reasons.TEAMMATES],
                lambda r: '-' not in r)])
        table = sorted(table, key=lambda x: x[1], reverse=True)
        for idx, line in enumerate(table):
            hero, value, reason = line
            output_table.append([idx + 1, self.web_data[hero]['cn_name'],
                                 round(value, 3), reason])
        _theirs_score = sum(theirs_score) / len(theirs_score)
        _ours_score = sum(ours_score) / len(ours_score)
        win_rate = _ours_score / (_ours_score + _theirs_score) * 100
        output_table.append([0, '胜率', win_rate, ''])
        return win_rate, output_table, table

    @staticmethod
    def get_cn_win_rate_output(win_rate, table):
        from data import COMPLETE_CUSTOM_DATA
        msg = '胜率:{0:.2f},易发挥:'.format(win_rate)
        h_list = []
        for i in range(3):
            hero = table[i][0]
            h_list.append(COMPLETE_CUSTOM_DATA['cn_short_abbrev'][hero])
        msg += ','.join(h_list)
        return msg

    @staticmethod
    def get_cn_recommend_output(v_list):
        from data import COMPLETE_CUSTOM_DATA
        msgs = []
        msg = '推荐:'
        h_list = []
        for i in range(15):
            h = v_list[i][0]
            h_list.append(COMPLETE_CUSTOM_DATA['cn_short_abbrev'][h])
        msg += ','.join(h_list)
        msgs.append(msg)
        msg = '不推荐:'
        h_list = []
        for i in range(15):
            h = v_list[-i - 1][0]
            h_list.append(COMPLETE_CUSTOM_DATA['cn_short_abbrev'][h])
        msg += ','.join(h_list)
        msgs.append(msg)
        return ';'.join(msgs)

    def get_reason(self, hero, reasons, reason, check):

        _reason = []
        for r in CN_REASON_DICT:
            if check(r) and hero in reasons[r]:
                if r == reason[0] or r == reason[1]:
                    _reason.append(CN_REASON_DICT[r] + ':' +
                                   ','.join([self.web_data[h]['cn_name']
                                             for h in reasons[r][hero]]))
                elif CN_REASON_DICT[r] not in _reason:
                    _reason.append(CN_REASON_DICT[r])

        return ';'.join(_reason)

    def get_recommend_table(self, v_list, reasons, n=15):
        table_good = [[0, '', '', '推荐']]
        for i in range(n):
            h = v_list[i][0]
            cn_name = self.web_data[h]['cn_name']
            table_good.append(
                [i + 1, cn_name, round(v_list[i][1], 3),
                 self.get_reason(h, reasons, [Reasons.MATCH_UPS,
                                              Reasons.TEAMMATES],
                                 lambda r: '-' not in r)])
        table_bad = [[0, '', '', '不推荐']]
        for i in range(n):
            h = v_list[-i - 1][0]
            cn_name = self.web_data[h]['cn_name']
            table_bad.append(
                [i + 1, cn_name, round(v_list[-i - 1][1], 3),
                 self.get_reason(h, reasons, [Reasons.N_MATCH_UPS,
                                              Reasons.N_TEAMMATES],
                                 lambda r: '-' in r)])
        table = table_good
        table.append([0, '', '', ''])
        table.extend(table_bad)
        return table

    def calculate_based_on_cfg(self, config_str):
        hero_value, reasons = self.init_value()

        # Based on win rate
        sorted_list = []
        for h in self.web_data:
            sorted_list.append(
                [h, self.web_data[h]['win_rate_' + config_str]])
        sorted_list = sorted(sorted_list, key=lambda x: x[1])
        hero_value = self.add_weight(hero_value, sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.WIN_RATE, sorted_list)

        # Based on match up index
        sorted_list = []
        inverse_dict = {}
        for h in self.web_data:
            total_pos = 0
            total_neg = 0
            for other in self.web_data[h]['match_ups_' + config_str]:
                index = self.web_data[h]['match_ups_' + config_str][other]
                if index > 0:
                    total_pos += index
                else:
                    total_neg += index
                if other not in inverse_dict:
                    inverse_dict[other] = 0
                inverse_dict[other] += -index
            sorted_list.append([h, total_pos, total_neg])
        _sorted_list = sorted(sorted_list, key=lambda x: x[1])
        hero_value = self.add_weight(hero_value, _sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.ANTI_INDEX_POS, _sorted_list)
        _sorted_list = sorted(sorted_list, key=lambda x: x[2])
        hero_value = self.add_weight(hero_value, _sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.ANTI_INDEX_NEG, _sorted_list)
        sorted_list = []
        for h in inverse_dict:
            sorted_list.append([h, inverse_dict[h]])
        sorted_list = sorted(sorted_list, key=lambda x: x[1])
        hero_value = self.add_weight(hero_value, sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.ANTI_INDEX, _sorted_list)

        # Based on teammate index
        sorted_list = []
        inverse_dict = {}
        for h in self.web_data:
            total_pos = 0
            total_neg = 0
            for other in self.web_data[h]['teammates_' + config_str]:
                index = self.web_data[h]['teammates_' + config_str][other]
                if index > 0:
                    total_pos += index
                else:
                    total_neg += index
                if other not in inverse_dict:
                    inverse_dict[other] = 0
                inverse_dict[other] += -index
            sorted_list.append([h, total_pos, total_neg])
        _sorted_list = sorted(sorted_list, key=lambda x: x[1])
        hero_value = self.add_weight(hero_value, _sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.COOP_INDEX_POS, _sorted_list)
        _sorted_list = sorted(sorted_list, key=lambda x: (x[2], x[1]))
        hero_value = self.add_weight(hero_value, _sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.COOP_INDEX_NEG, _sorted_list)
        sorted_list = []
        for h in inverse_dict:
            sorted_list.append([h, inverse_dict[h]])
        sorted_list = sorted(sorted_list, key=lambda x: x[1])
        hero_value = self.add_weight(hero_value, sorted_list, 0.5)
        self.collect_reason(reasons, Reasons.COOP_INDEX, _sorted_list)
        return hero_value, reasons

    def cal_match(self, config_str, hero_value, reasons,
                  match_ups, teammates):
        hero_value = copy.deepcopy(hero_value)
        reasons = copy.deepcopy(reasons)
        reasons[Reasons.N_MATCH_UPS] = {}
        reasons[Reasons.MATCH_UPS] = {}
        reasons[Reasons.N_TEAMMATES] = {}
        reasons[Reasons.TEAMMATES] = {}
        for hero in match_ups:
            sorted_list = []
            for other in self.web_data[hero]['match_ups_' + config_str]:
                sorted_list.append([other, -self.web_data[hero]
                ['match_ups_' + config_str][other]])
            sorted_list = sorted(sorted_list, key=lambda x: x[1])
            hero_value = self.add_weight(hero_value, sorted_list, 1.0)
            self.collect_match_reason(reasons, Reasons.MATCH_UPS,
                                      sorted_list, hero)

            sorted_list = []
            for other in self.web_data:
                if other == hero:
                    continue
                sorted_list.append([other, self.web_data[other]
                ['c_match_ups_' + config_str][hero]])
            sorted_list = sorted(sorted_list, key=lambda x: x[1])
            hero_value = self.add_weight(hero_value, sorted_list, 1.0)
            self.collect_match_reason(reasons, Reasons.MATCH_UPS,
                                      sorted_list, hero)

        for hero in teammates:
            sorted_list = []
            for other in self.web_data[hero]['teammates_' + config_str]:
                sorted_list.append([other, self.web_data[hero]
                ['teammates_' + config_str][other]])
            sorted_list = sorted(sorted_list, key=lambda x: x[1])
            hero_value = self.add_weight(hero_value, sorted_list, 0.8)
            self.collect_match_reason(reasons, Reasons.TEAMMATES,
                                      sorted_list, hero)
        return hero_value, reasons

    def cal_role(self, hero_value, roles):
        hero_value = copy.deepcopy(hero_value)
        for role in roles:
            sorted_list = []
            for hero in self.web_data:
                value = self.web_data[hero]['role'][role]
                sorted_list.append([hero, value])
            sorted_list = sorted(sorted_list, key=lambda x: x[1])
            hero_value = self.add_weight_by_set(hero_value, sorted_list,
                                                1.0)
        return hero_value


if __name__ == '__main__':
    from dpapi.custom_lib.cn_heroes import Heroes

    # TODO: Fix this

    core = Core()
    core.load_data()
    cfg = {
        'config_str': 'cn_h_y',
        'roles': ['Carry', 'Support']
    }
    match_ups = [Heroes.none, Heroes.none, Heroes.none,
                 Heroes.none, Heroes.none]
    teammates = [Heroes.none, Heroes.none, Heroes.none,
                 Heroes.none, Heroes.none]
    match_ups, teammates = core.remove_none(match_ups, teammates)
    r = core.calculate(cfg, match_ups, teammates, list(core.name_dict.keys()))
    print(r)
