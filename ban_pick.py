import json

with open('data.json', 'r') as f:
    data = json.load(f)

h_wr = []
for h in data:
    h_wr.append([h, data[h]['win_rate']])

h_wr = sorted(h_wr, key=lambda x: x[1], reverse=True)
for i in range(10):
    print(data[h_wr[i][0]]['name'], h_wr[i][1])

print()

match_ups = []
teammates = []

match_up = 'Broodmother'
h_n = [h for h in data if data[h]['name'] == match_up][0]
_match_ups = data[h_n]['match_ups']

h_match_ups = []
for h, ai in _match_ups.items():
    h_match_ups.append([h, ai])

h_anti = sorted(h_match_ups, key=lambda x: x[1], reverse=True)
for i in range(10):
    print(data[h_anti[i][0]]['name'], h_anti[i][1])
