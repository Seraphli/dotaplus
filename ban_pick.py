from tabulate import tabulate
import json
import numpy as np

with open('data.json', 'r') as f:
    data = json.load(f)

num_heroes = len(data.keys())
factor = np.arange(num_heroes, 0, -1)
factor = -np.log(factor / np.sum(factor))
h_v = {}
for h in data:
    h_v[h] = 0

print('Heroes List')
table = []
for h in data:
    table.append([data[h]['name']])
print(tabulate(table, headers=['Name'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))


def apply_factor(sorted_list, f=1.0):
    for idx, _h in enumerate(sorted_list):
        _h = _h[0]
        h_v[_h] += f * factor[idx]


def print_v_list(exclude=None):
    if exclude:
        _num = num_heroes - len(exclude)
    else:
        _num = num_heroes
    v_list = []
    for _h, _v in h_v.items():
        if exclude and _h in exclude:
            continue
        v_list.append([_h, _v])
    v_list = sorted(v_list, key=lambda x: x[1], reverse=True)
    print('Recommended')
    table = []
    for i in range(20):
        table.append([data[v_list[i][0]]['name'], v_list[i][1]])
    print(tabulate(table, headers=['Name', 'Value'],
                   tablefmt='psql', floatfmt='.2f', showindex='always'))
    print('Not Recommended')
    table = []
    for i in range(20):
        table.append([data[v_list[_num - i - 1][0]]['name'],
                      v_list[_num - i - 1][1]])
    print(tabulate(table, headers=['Name', 'Value'],
                   tablefmt='psql', floatfmt='.2f', showindex='always'))


def recommend(match_ups, teammates):
    # TODO: recommend by game
    _list = []
    for mu in match_ups:
        _list.append([h for h in data if data[h]['name'] == mu][0])
    match_ups = _list
    _list = []
    for tm in teammates:
        _list.append([h for h in data if data[h]['name'] == tm][0])
    teammates = _list
    for mu in match_ups:
        mu_index = []
        for _mu in data[mu]['match_ups']:
            mu_index.append([_mu, -data[mu]['match_ups'][_mu]])
        mu_index = sorted(mu_index, key=lambda x: x[1])
        apply_factor(mu_index, 1.0)

        mu_index = []
        for h in data:
            if h == mu:
                continue
            mu_index.append([h, data[h]['match_ups'][mu]])
        mu_index = sorted(mu_index, key=lambda x: x[1])
        apply_factor(mu_index, 1.0)

    for tm in teammates:
        tm_index = []
        for _tm in data[tm]['teammates']:
            tm_index.append([_tm, data[tm]['match_ups'][_tm]])
        tm_index = sorted(tm_index, key=lambda x: x[1])
        apply_factor(tm_index, 0.8)

    exclude = []
    exclude.extend(match_ups)
    exclude.extend(teammates)
    print_v_list(exclude)


def pre_calculated():
    h_wr = []
    for h in data:
        h_wr.append([h, data[h]['win_rate']])
    h_wr = sorted(h_wr, key=lambda x: x[1])
    apply_factor(h_wr, 0.5)

    h_mu = []
    h_mu_dict = {}
    for h in data:
        total_pos = 0
        total_neg = 0
        for mu in data[h]['match_ups']:
            anti_index = data[h]['match_ups'][mu]
            if anti_index > 0:
                total_pos += anti_index
            else:
                total_neg += anti_index
            if mu not in h_mu_dict:
                h_mu_dict[mu] = 0
            h_mu_dict[mu] += -anti_index
        h_mu.append([h, total_pos, total_neg])
    h_mu_pos = sorted(h_mu, key=lambda x: x[1])
    apply_factor(h_mu_pos, 0.3)
    h_mu_neg = sorted(h_mu, key=lambda x: x[2])
    apply_factor(h_mu_neg, 0.3)
    h_mu = []
    for h in h_mu_dict:
        h_mu.append([h, h_mu_dict[h]])
    h_mu = sorted(h_mu, key=lambda x: x[1])
    apply_factor(h_mu, 0.3)

    h_tm = []
    h_tm_dict = {}
    for h in data:
        total_pos = 0
        total_neg = 0
        for tm in data[h]['teammates']:
            coop_index = data[h]['teammates'][tm]
            if coop_index > 0:
                total_pos += coop_index
            else:
                total_neg += coop_index
            if tm not in h_tm_dict:
                h_tm_dict[tm] = 0
            h_tm_dict[tm] += coop_index
        h_tm.append([h, total_pos, total_neg])
    h_tm_pos = sorted(h_tm, key=lambda x: x[1])
    apply_factor(h_tm_pos, 0.3)
    h_tm_neg = sorted(h_tm, key=lambda x: (x[2], x[1]))
    apply_factor(h_tm_neg, 0.3)
    h_tm = []
    for h in h_tm_dict:
        h_tm.append([h, h_tm_dict[h]])
    h_tm = sorted(h_tm, key=lambda x: x[1])
    apply_factor(h_tm, 0.3)

    print_v_list()


pre_calculated()
print()
recommend(
    match_ups=['Ember Spirit', 'Juggernaut', 'Axe', 'Lich', 'Windranger'],
    teammates=['Storm Spirit', 'Phantom Assassin', 'Underlord',
               'Ancient Apparition'])
