import json

with open('scrapy/dotaplus/heroes.json', 'r') as f:
    heroes = json.load(f)

h_wr = []
name_dict = {}
for h in heroes:
    h_wr.append([h['hero_real_name'], h['win_rate']])
    name_dict[h['hero_name']] = h['hero_real_name']

h_wr = sorted(h_wr, key=lambda x: x[1], reverse=True)
for i in range(10):
    print(h_wr[i][0], h_wr[i][1])

print()

match_ups = []
teammates = []

match_up = 'Broodmother'
anti = [h for h in heroes if h['hero_real_name'] == match_up][0]['anti']

h_anti = []
for h, ai in anti.items():
    h_anti.append([h, ai])

h_anti = sorted(h_anti, key=lambda x: x[1], reverse=True)
for i in range(10):
    print(name_dict[h_anti[i][0]], h_anti[i][1])
