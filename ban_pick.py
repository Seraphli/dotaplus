from tabulate import tabulate
import json

with open('data.json', 'r') as f:
    data = json.load(f)

print('Based on win rate')
h_wr = []
for h in data:
    h_wr.append([h, data[h]['win_rate']])
print('Recommended')
h_wr = sorted(h_wr, key=lambda x: x[1], reverse=True)
table = []
for i in range(5):
    table.append([data[h_wr[i][0]]['name'], h_wr[i][1]])
print(tabulate(table, headers=['Name', 'Win Rate'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
print('Not Recommended')
h_wr = sorted(h_wr, key=lambda x: x[1])
table = []
for i in range(5):
    table.append([data[h_wr[i][0]]['name'], h_wr[i][1]])
print(tabulate(table, headers=['Name', 'Win Rate'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
print()

print('Based on match ups')
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
print('Recommended')
h_mu_pos = sorted(h_mu, key=lambda x: x[1], reverse=True)
table = []
for i in range(5):
    table.append([data[h_mu_pos[i][0]]['name'], h_mu_pos[i][1]])
print(tabulate(table, headers=['Name', 'Total Positive'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
h_mu_neg = sorted(h_mu, key=lambda x: x[2], reverse=True)
table = []
for i in range(5):
    table.append([data[h_mu_neg[i][0]]['name'], h_mu_neg[i][2]])
print(tabulate(table, headers=['Name', 'Total Negative'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
print('Not Recommended')
h_mu_pos = sorted(h_mu, key=lambda x: x[1])
table = []
for i in range(5):
    table.append([data[h_mu_pos[i][0]]['name'], h_mu_pos[i][1]])
print(tabulate(table, headers=['Name', 'Total Positive'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
h_mu_neg = sorted(h_mu, key=lambda x: x[2])
table = []
for i in range(5):
    table.append([data[h_mu_neg[i][0]]['name'], h_mu_neg[i][2]])
print(tabulate(table, headers=['Name', 'Total Negative'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
print()

print('Based on teammates')
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
print('Recommended')
h_tm_pos = sorted(h_tm, key=lambda x: x[1], reverse=True)
table = []
for i in range(5):
    table.append([data[h_tm_pos[i][0]]['name'], h_tm_pos[i][1]])
print(tabulate(table, headers=['Name', 'Total Positive'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
h_tm_neg = sorted(h_tm, key=lambda x: (x[2], x[1]), reverse=True)
table = []
for i in range(5):
    table.append([data[h_tm_neg[i][0]]['name'], h_tm_neg[i][2]])
print(tabulate(table, headers=['Name', 'Total Negative'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
print('Not Recommended')
h_tm_pos = sorted(h_tm, key=lambda x: x[1])
table = []
for i in range(5):
    table.append([data[h_tm_pos[i][0]]['name'], h_tm_pos[i][1]])
print(tabulate(table, headers=['Name', 'Total Positive'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
h_tm_neg = sorted(h_tm, key=lambda x: (x[2], x[1]))
table = []
for i in range(5):
    table.append([data[h_tm_neg[i][0]]['name'], h_tm_neg[i][2]])
print(tabulate(table, headers=['Name', 'Total Negative'],
               tablefmt='psql', floatfmt='.2f', showindex='always'))
print()
