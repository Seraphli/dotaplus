import urllib
import tornado.httpclient
from cn_heroes import CNAbbrevHeroes
import json
from ban_pick import BanPick

bp = BanPick()

team_no = 0
teams = [[CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none],
         [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none]]
bans = []

available = list(bp.data.keys())
for ban in bans:
    available.remove(ban)
for team in teams:
    for h in team:
        if h in available:
            available.remove(h)

post_data = {
    'team_no': json.dumps(team_no),
    'teams': json.dumps(teams),
    'available': json.dumps(available)
}
body = urllib.parse.urlencode(post_data)
http_client = tornado.httpclient.HTTPClient()
response = http_client.fetch('http://127.0.0.1:30207/bp',
                             method='POST', body=body)
resp = json.loads(response.body.decode())
print(resp)
