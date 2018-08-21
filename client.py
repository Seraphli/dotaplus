import urllib
import tornado.httpclient
from cn_heroes import CNAbbrevHeroes

team_no = 0
teams = [[CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none],
         [CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none, CNAbbrevHeroes.none,
          CNAbbrevHeroes.none]]
bans = []

post_data = {
    'team_no': team_no,
    'teams': teams,
    'bans': bans
}
body = urllib.parse.urlencode(post_data)
http_client = tornado.httpclient.HTTPClient()
response = http_client.fetch('http://127.0.0.1:8888/bp',
                             method='POST', body=body)
print(eval(response.body.decode()))
