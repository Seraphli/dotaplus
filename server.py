import tornado.ioloop
import tornado.web
from ban_pick import BanPick
from output import CNOutput
import get_data
import multiprocessing as mp
import time
import json


class BPHandler(tornado.web.RequestHandler):
    def initialize(self):
        self.bp = BanPick()
        self.o = CNOutput()
        self.last_time = time.time()

    def post(self):
        if time.time() - self.last_time > 43200:
            self.bp = BanPick()
            self.last_time = time.time()

        team_no = json.loads(self.get_argument('team_no'))
        teams = json.loads(self.get_argument('teams'))
        available = json.loads(self.get_argument('available'))
        teammates = teams[team_no]
        match_ups = teams[1 - team_no]
        match_ups, teammates = self.bp.remove_none(match_ups, teammates)
        r = self.bp.recommend_dict(match_ups, teammates, available)
        if r is not None:
            r['output'] = self.o.recommend_str(match_ups, teammates, available)
            self.write(json.dumps(r))
        r = self.bp.win_rate_dict(match_ups, teammates)
        if r is not None:
            r['output'] = self.o.win_rate_str(match_ups, teammates)
            self.write(json.dumps(r))


def update_data():
    print('Update data')
    get_data.main()
    print('Update complete')
    time.sleep(43200)
    mp.Process(target=update_data).start()


def make_app():
    return tornado.web.Application([
        (r'/bp', BPHandler),
    ])


if __name__ == "__main__":
    mp.Process(target=update_data).start()
    time.sleep(20)
    print('Server start')
    app = make_app()
    app.listen(30207)
    tornado.ioloop.IOLoop.current().start()
