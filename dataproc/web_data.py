import os
import json
import copy


class WebData(object):
    def __init__(self):
        from spider.dotaplus.dotaplus.spiders.dotamax import NameDictSpider, \
            CNNameDictSpider, WinRateSpider, MatchUpsSpider, TeammatesSpider
        from spider.dotaplus.dotaplus.spiders.dotawiki import CountersSpider
        from util.util import get_path
        self.spiders = [NameDictSpider, CNNameDictSpider, WinRateSpider,
                        MatchUpsSpider, TeammatesSpider, CountersSpider]

        self.spider_names = []
        self.file_names = []
        for spider in self.spiders:
            self.spider_names.append(spider.name)
            self.file_names.append(spider.custom_settings['FEED_URI'])
        self.original_cwd = os.getcwd()
        self.spider_path = get_path('spider/dotaplus', parent=True)
        self.raw_data = {}
        self.data = {}
        self.name_dict = {}

    def crawl_data(self):
        os.chdir(self.spider_path)
        self._crawl()
        self.load_json()
        os.chdir(self.original_cwd)
        self.process_data()
        self.insert_role_into_data()
        self.save_data()

    def _crawl(self):
        from scrapy.utils.project import get_project_settings
        from twisted.internet import reactor
        from scrapy.crawler import CrawlerRunner
        from scrapy.utils.log import configure_logging
        from util.util import remove_files
        remove_files(self.file_names)
        settings = get_project_settings()
        settings.set('LOG_ENABLED', False)
        configure_logging(settings)
        runner = CrawlerRunner()
        for spider in self.spiders:
            runner.crawl(spider)
        d = runner.join()
        d.addBoth(lambda _: reactor.stop())
        reactor.run()
        print('Data collect complete.')

    def load_json(self):
        self.raw_data = {}
        for idx, n in enumerate(self.spider_names):
            with open(self.file_names[idx], 'r') as f:
                self.raw_data[n] = json.load(f)

    def process_data(self):
        self.combine_data()
        self.combine_counter()

    def combine_data(self):
        self.data = {}
        self.name_dict = {}
        # Collect name
        for nd in self.raw_data['name_dict']:
            self.data[nd['hero_name']] = {'name': nd['hero_real_name']}
            self.name_dict[nd['hero_real_name']] = nd['hero_name']
        for nd in self.raw_data['cn_name_dict']:
            self.data[nd['hero_name']]['cn_name'] = nd['hero_real_name']

        # Data from dotamax
        for wr in self.raw_data['win_rate']:
            cfg = list(wr.keys())
            cfg.remove('hero_name')
            for _key in cfg:
                self.data[wr['hero_name']][_key] = wr[_key]
        for mu in self.raw_data['match_ups']:
            cfg = list(mu.keys())
            cfg.remove('hero_name')
            for _key in cfg:
                self.data[mu['hero_name']][_key] = mu[_key]
        for tm in self.raw_data['teammates']:
            cfg = list(tm.keys())
            cfg.remove('hero_name')
            for _key in cfg:
                self.data[tm['hero_name']][_key] = tm[_key]

        # Data from dotawiki
        for counter in self.raw_data['counters']:
            h = self.name_dict[counter['hero_name']]
            _counter = {}
            for k in counter['counters']:
                _heroes = []
                for h_name in counter['counters'][k]:
                    _heroes.append(self.name_dict[h_name])
                _counter[k] = _heroes
            self.data[h]['counters'] = _counter

    def combine_counter(self):
        for h in self.data:
            for key in list(self.data[h].keys()):
                if 'match_ups' in key:
                    c_key = 'c_' + key
                    self.data[h][c_key] = copy.deepcopy(self.data[h][key])
                    for mu in self.data[h][c_key]:
                        if mu in self.data[h]['counters']['good_against']:
                            self.data[h][c_key][mu] += 5.0
                            self.data[h][c_key][mu] = round(
                                self.data[h][c_key][mu], 2)
                        if mu in self.data[h]['counters']['bad_against']:
                            self.data[h][c_key][mu] -= 5.0
                            self.data[h][c_key][mu] = round(
                                self.data[h][c_key][mu], 2)
            for key in list(self.data[h].keys()):
                if 'teammates' in key:
                    c_key = 'c_' + key
                    self.data[h][c_key] = copy.deepcopy(self.data[h][key])
                    for tm in self.data[h][c_key]:
                        if tm in self.data[h]['counters']['work_well']:
                            self.data[h][c_key][tm] += 5.0
                            self.data[h][c_key][tm] = round(
                                self.data[h][c_key][tm], 2)

    def insert_role_into_data(self):
        from util.util import get_path
        with open(get_path('data') + '/role.json', 'r') as f:
            roles = json.load(f)
        for k in self.data.keys():
            self.data[k]['role'] = roles[k]

    def save_data(self):
        from util.util import get_path
        import shutil

        with open(get_path('data') + '/data.json', 'w') as f:
            json.dump(self.data, f)
        shutil.copy(get_path('data') + '/data.json', get_path('server_data'))


if __name__ == '__main__':
    wd = WebData()
    wd.crawl_data()
