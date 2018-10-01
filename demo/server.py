import tornado.ioloop
import tornado.web
import tornado.options
import time
import json
from dataproc.core import Core
from util.util import get_path

core = Core()
core.load_data(get_path('server_data', parent=True)
               + '/data.json')
last_time = time.time()


class BPHandler(tornado.web.RequestHandler):
    def initialize(self):
        pass

    def load_data(self):
        global core, last_time
        core.load_data(get_path('server_data', parent=True)
                       + '/data.json')
        last_time = time.time()

    def check_update(self):
        global last_time
        if time.time() - last_time > 43200:
            print('{}, Reload data'.format(time.time()))
            self.load_data()

    def post(self):
        global core
        self.check_update()
        team_no = json.loads(self.get_argument('team_no'))
        teams = json.loads(self.get_argument('teams'))
        available = json.loads(self.get_argument('available'))
        cfg = json.loads(self.get_argument('cfg'))
        teammates = teams[team_no]
        match_ups = teams[1 - team_no]
        match_ups, teammates = core.remove_none(match_ups, teammates)
        r = core.calculate(cfg, match_ups, teammates, available)
        response = {
            'table': r['table'],
            'output': r['output']
        }
        self.write(json.dumps(response))


def make_app():
    return tornado.web.Application([
        (r'/bp', BPHandler),
    ])


if __name__ == "__main__":
    print('{}, Server start'.format(time.time()))
    tornado.options.parse_command_line()
    app = make_app()
    app.listen(30207)
    tornado.ioloop.IOLoop.current().start()
