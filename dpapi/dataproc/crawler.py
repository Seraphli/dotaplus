from dpapi.spider.dotaplus.dotaplus.spiders.dotamax import NameDictSpider, \
    CNNameDictSpider, WinRateSpider, MatchUpsSpider, TeammatesSpider
from dpapi.spider.dotaplus.dotaplus.spiders.dotawiki import CountersSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os
import json
import copy
from dpapi.util.util import get_path
from multiprocessing import Process, Queue
import codecs


def f(_q, _setting, _spider):
    try:
        _p = CrawlerProcess(_setting)
        _p.crawl(_spider)
        _p.start(stop_after_crawl=True)
        _q.put(None)
    except Exception as e:
        _q.put(e)


class Crawler(object):
    def __init__(self, debug=False):
        self.debug = debug
        nd = get_path('data/generated', parent=True) + '/name_dict.json'
        with codecs.open(nd) as f:
            self.name_dict = json.load(f)

        nd = get_path('data/generated', parent=True) + '/hero_info.json'
        with codecs.open(nd) as f:
            self.hero_role = json.load(f)

        self.spiders = [
            WinRateSpider,
            MatchUpsSpider,
            TeammatesSpider,
            CountersSpider,
        ]
        self.spider_names = []
        self.file_names = []
        self.raw_data = {}
        settings = get_project_settings()
        settings.set('LOG_ENABLED', self.debug)
        settings.set('RETRY_TIMES', 10)
        settings.set('HTTPCACHE_ENABLED', True)
        settings.set('HTTPCACHE_EXPIRATION_SECS', 3600)
        self.settings = settings
        self.spider_project_path = get_path('spider/dotaplus', parent=True)
        self.data_path = get_path('data/server', parent=True)

    def load_json(self):
        self.raw_data = {}
        for idx, n in enumerate(self.spider_names):
            with open(self.file_names[idx], 'r') as f:
                self.raw_data[n] = json.load(f)

    def remove_json(self):
        for fn in self.file_names:
            if os.path.exists(fn):
                os.remove(fn)

    def prepare(self):
        self.spider_names = []
        self.file_names = []
        for spider in self.spiders:
            self.spider_names.append(spider.name)
            self.file_names.append(spider.custom_settings['FEED_URI'])

    def crawl(self):
        def _crawl(_spider):
            q = Queue()
            p = Process(target=f, args=(q, self.settings, _spider))
            p.start()
            result = q.get()
            p.join()
            if result is not None:
                raise result

        self.remove_json()
        for spider in self.spiders:
            _crawl(spider)
            print('.', end='', flush=True)
        print()
        return

    def process_data(self):
        _data = {}
        _name_dict = {}
        for hero_name in self.name_dict.keys():
            _data[hero_name] = {
                'name': self.name_dict[hero_name]['english'],
                'cn_name': self.name_dict[hero_name]['schinese'],
            }
            _name_dict[self.name_dict[hero_name]['english']] = hero_name
        for wr in self.raw_data['win_rate']:
            cfg = list(wr.keys())
            cfg.remove('hero_name')
            _data[wr['hero_name']][cfg[0]] = wr[cfg[0]]
        for mu in self.raw_data['match_ups']:
            cfg = list(mu.keys())
            cfg.remove('hero_name')
            _data[mu['hero_name']][cfg[0]] = mu[cfg[0]]
        for tm in self.raw_data['teammates']:
            cfg = list(tm.keys())
            cfg.remove('hero_name')
            _data[tm['hero_name']][cfg[0]] = tm[cfg[0]]
        for counter in self.raw_data['counters']:
            h = _name_dict[counter['hero_name']]
            _counter = {}
            for k in counter['counters']:
                _heroes = []
                for h_name in counter['counters'][k]:
                    _heroes.append(_name_dict[h_name])
                _counter[k] = _heroes
            _data[h]['counters'] = _counter
        for h in _data:
            for key in list(_data[h].keys()):
                if 'match_ups' in key:
                    c_key = 'c_' + key
                    _data[h][c_key] = copy.deepcopy(_data[h][key])
                    for mu in _data[h][c_key]:
                        if mu in _data[h]['counters']['good_against']:
                            _data[h][c_key][mu] += 5.0
                            _data[h][c_key][mu] = round(_data[h][c_key][mu], 2)
                        if mu in _data[h]['counters']['bad_against']:
                            _data[h][c_key][mu] -= 5.0
                            _data[h][c_key][mu] = round(_data[h][c_key][mu], 2)
            for key in list(_data[h].keys()):
                if 'match_ups' in key:
                    c_key = 'c_' + key
                    _data[h][c_key] = copy.deepcopy(_data[h][key])
                    for tm in _data[h][c_key]:
                        if tm in _data[h]['counters']['work_well']:
                            _data[h][c_key][tm] += 5.0
                            _data[h][c_key][tm] = round(_data[h][c_key][tm], 2)
        for hero_name in self.name_dict.keys():
            _data[hero_name]['role'] = self.hero_role[hero_name]
        with codecs.open(self.data_path + '/web_data.json', 'w') as f:
            json.dump(_data, f)

    def run(self):
        original_cwd = os.getcwd()
        os.chdir(self.spider_project_path)
        self.prepare()
        print('Crawling data...')
        self.crawl()
        self.load_json()
        os.chdir(original_cwd)
        print('Processing data...')
        self.process_data()
