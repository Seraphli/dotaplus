def crawl_web_data(debug=False):
    from spider.dotaplus.dotaplus.spiders.dotamax import NameDictSpider, \
        CNNameDictSpider, WinRateSpider, MatchUpsSpider, TeammatesSpider
    from spider.dotaplus.dotaplus.spiders.dotawiki import CountersSpider
    from scrapy.crawler import CrawlerProcess
    from scrapy.utils.project import get_project_settings
    import os
    import json
    import pickle
    import copy
    from util.util import get_path

    def load_json(_spider_names, _file_names):
        _raw_data = {}
        for idx, n in enumerate(_spider_names):
            with open(_file_names[idx], 'r') as f:
                _raw_data[n] = json.load(f)
        return _raw_data

    def remove_json(_file_names):
        for fn in _file_names:
            if os.path.exists(fn):
                os.remove(fn)

    def prepare(_spiders):
        _spider_names = []
        _file_names = []
        for spider in _spiders:
            _spider_names.append(spider.name)
            _file_names.append(spider.custom_settings['FEED_URI'])
        return _spider_names, _file_names

    def crawl(_spiders, _file_names):
        remove_json(_file_names)
        settings = get_project_settings()
        settings.set('LOG_ENABLED', debug)
        settings.set('RETRY_TIMES', 10)
        process = CrawlerProcess(settings)
        for spider in _spiders:
            process.crawl(spider)
        process.start(stop_after_crawl=True)
        return

    def process_data(_raw_data):
        _data = {}
        _name_dict = {}
        for nd in _raw_data['name_dict']:
            _data[nd['hero_name']] = {
                'name': nd['hero_real_name'],
            }
            _name_dict[nd['hero_real_name']] = nd['hero_name']
        for nd in _raw_data['cn_name_dict']:
            _data[nd['hero_name']]['cn_name'] = nd['hero_real_name']
        for wr in _raw_data['win_rate']:
            cfg = list(wr.keys())
            cfg.remove('hero_name')
            _data[wr['hero_name']][cfg[0]] = wr[cfg[0]]
        for mu in _raw_data['match_ups']:
            cfg = list(mu.keys())
            cfg.remove('hero_name')
            _data[mu['hero_name']][cfg[0]] = mu[cfg[0]]
        for tm in _raw_data['teammates']:
            cfg = list(tm.keys())
            cfg.remove('hero_name')
            _data[tm['hero_name']][cfg[0]] = tm[cfg[0]]
        for counter in _raw_data['counters']:
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
                            _data[h][c_key][mu] = round(
                                _data[h][c_key][mu], 2)
                        if mu in _data[h]['counters']['bad_against']:
                            _data[h][c_key][mu] -= 5.0
                            _data[h][c_key][mu] = round(
                                _data[h][c_key][mu], 2)
            for key in list(_data[h].keys()):
                if 'match_ups' in key:
                    c_key = 'c_' + key
                    _data[h][c_key] = copy.deepcopy(_data[h][key])
                    for tm in _data[h][c_key]:
                        if tm in _data[h]['counters']['work_well']:
                            _data[h][c_key][tm] += 5.0
                            _data[h][c_key][tm] = round(
                                _data[h][c_key][tm], 2)
        with open(get_path('server_data', parent=True) + '/data.pkl',
                  'wb') as f:
            pickle.dump(_data, f)

    spiders = [
        NameDictSpider,
        CNNameDictSpider,
        WinRateSpider,
        MatchUpsSpider,
        TeammatesSpider,
        CountersSpider,
    ]
    original_cwd = os.getcwd()
    project_path = get_path('spider/dotaplus', parent=True)
    os.chdir(project_path)
    spider_names, file_names = prepare(spiders)
    print('Crawling data...')
    crawl(spiders, file_names)
    raw_data = load_json(spider_names, file_names)
    os.chdir(original_cwd)
    print('Processing data...')
    process_data(raw_data)


def main():
    crawl_web_data(debug=False)


if __name__ == '__main__':
    main()
