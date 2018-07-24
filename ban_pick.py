import json

with open('scrapy/dotaplus/heroes.json', 'r') as f:
    heroes = json.load(f)

h_wr = []
for h in heroes:
    h_wr.append([h['hero_name'], h['win_rate']])

h_wr = sorted(h_wr, key=lambda x: x[1], reverse=True)
for i in range(10):
    print(h_wr[i][0], h_wr[i][1])

print()

match_ups = []
teammates = []

match_up = 'zuus'
anti = [h for h in heroes if h['hero_name'] == 'zuus'][0]['anti']

h_anti = []
for h, ai in anti.items():
    h_anti.append([h, ai])

h_anti = sorted(h_anti, key=lambda x: x[1], reverse=True)
for i in range(10):
    print(h_anti[i][0], h_anti[i][1])
