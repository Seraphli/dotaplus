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


def recommend(match_ups, teammates):
    # TODO: recommend by game
    pass


def pre_calculated():
    h_wr = []
    for h in data:
        h_wr.append([h, data[h]['win_rate']])
    h_wr = sorted(h_wr, key=lambda x: x[1])
    for idx, _h in enumerate(h_wr):
        _h = _h[0]
        h_v[_h] += factor[idx]

    h_mu = []
    for h in data:
        total_pos = 0
        total_neg = 0
        for mu in data[h]['match_ups']:
            anti_index = data[h]['match_ups'][mu]
            if anti_index > 0:
                total_pos += anti_index
            else:
                total_neg += anti_index
        h_mu.append([h, total_pos, total_neg])
    h_mu_pos = sorted(h_mu, key=lambda x: x[1])
    for idx, _h in enumerate(h_mu_pos):
        _h = _h[0]
        h_v[_h] += factor[idx]
    h_mu_neg = sorted(h_mu, key=lambda x: x[2])
    for idx, _h in enumerate(h_mu_neg):
        _h = _h[0]
        h_v[_h] += factor[idx]

    h_tm = []
    for h in data:
        total_pos = 0
        total_neg = 0
        for tm in data[h]['teammates']:
            coop_index = data[h]['teammates'][tm]
            if coop_index > 0:
                total_pos += coop_index
            else:
                total_neg += coop_index
        h_tm.append([h, total_pos, total_neg])
    h_tm_pos = sorted(h_tm, key=lambda x: x[1])
    for idx, _h in enumerate(h_tm_pos):
        _h = _h[0]
        h_v[_h] += factor[idx]
    h_tm_neg = sorted(h_tm, key=lambda x: (x[2], x[1]))
    for idx, _h in enumerate(h_tm_neg):
        _h = _h[0]
        h_v[_h] += factor[idx]

    v_list = []
    for _h, _v in h_v.items():
        v_list.append([_h, _v])
    v_list = sorted(v_list, key=lambda x: x[1], reverse=True)
    print('Recommended')
    table = []
    for i in range(10):
        table.append([data[v_list[i][0]]['name'], v_list[i][1]])
    print(tabulate(table, headers=['Name', 'Value'],
                   tablefmt='psql', floatfmt='.2f', showindex='always'))
    print('Not Recommended')
    table = []
    for i in range(10):
        table.append([data[v_list[num_heroes - i - 1][0]]['name'],
                      v_list[num_heroes - i - 1][1]])
    print(tabulate(table, headers=['Name', 'Value'],
                   tablefmt='psql', floatfmt='.2f', showindex='always'))


pre_calculated()
