import tornado.ioloop
import tornado.web
from ban_pick import BanPick
import get_data
import multiprocessing as mp
import time
import json


class BPHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bp = BanPick()

    def post(self):
        team_no = json.loads(self.get_argument('team_no'))
        teams = json.loads(self.get_argument('teams'))
        bans = json.loads(self.get_argument('bans'))
        available = list(self.bp.data.keys())
        for ban in bans:
            print(ban)
            available.remove(ban)
        for team in teams:
            for h in team:
                if h in available:
                    available.remove(h)
        teammates = teams[team_no]
        match_ups = teams[1 - team_no]
        match_ups, teammates = self.bp.remove_none(match_ups, teammates)
        r = self.bp.recommend_dict(match_ups, teammates, available)
        if r is not None:
            self.write(json.dumps(r))
        r = self.bp.win_rate_dict(match_ups, teammates)
        if r is not None:
            self.write(json.dumps(r))


def update_data():
    print('Update data')
    get_data.main()
    time.sleep(60)


def make_app():
    return tornado.web.Application([
        (r"/bp", BPHandler),
    ])


if __name__ == "__main__":
    mp.Process(target=update_data).start()
    time.sleep(60)
    print('Server start')
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
