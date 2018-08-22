import urllib
import tornado.httpclient
from cn_heroes import CNAbbrevHeroes
import json

team_no = 0
teams = [[CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none],
         [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none]]
bans = []

post_data = {
    'team_no': json.dumps(team_no),
    'teams': json.dumps(teams),
    'bans': json.dumps(bans)
}
body = urllib.parse.urlencode(post_data)
http_client = tornado.httpclient.HTTPClient()
response = http_client.fetch('http://127.0.0.1:30207/bp',
                             method='POST', body=body)
resp = json.loads(response.body.decode())
print(resp)
