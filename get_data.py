from util import get_path
import os
import json
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.dotaplus.dotaplus.spiders.dotamax import NameDictSpider, \
    WinRateSpider, MatchUpsSpider, TeammatesSpider


def remove_json(file_names):
    for fn in file_names:
        if os.path.exists(fn):
            os.remove(fn)


def load_json(names, file_names):
    raw_data = {}
    for idx, n in enumerate(names):
        with open(file_names[idx], 'r') as f:
            raw_data[n] = json.load(f)
    return raw_data


def crawl(spiders):
    spider_names = []
    file_names = []
    for spider in spiders:
        spider_names.append(spider.name)
        file_names.append(spider.custom_settings['FEED_URI'])
    remove_json(file_names)
    settings = get_project_settings()
    settings.set('LOG_ENABLED', False)
    process = CrawlerProcess(settings)
    for spider in spiders:
        process.crawl(spider)
    process.start()
    return load_json(spider_names, file_names)


def process_data(raw_data):
    data = {}
    for nd in raw_data['name_dict']:
        data[nd['hero_name']] = {
            'name': nd['hero_real_name'],
        }
    for wr in raw_data['win_rate']:
        data[wr['hero_name']]['win_rate'] = wr['win_rate']
    for mu in raw_data['match_ups']:
        data[mu['hero_name']]['match_ups'] = mu['match_ups']
    for tm in raw_data['teammates']:
        data[tm['hero_name']]['teammates'] = tm['teammates']
    with open('data.json', 'w') as f:
        json.dump(data, f)


def main():
    spiders = [NameDictSpider, WinRateSpider, MatchUpsSpider, TeammatesSpider]
    original_cwd = os.getcwd()
    project_path = get_path('spider/dotaplus')
    os.chdir(project_path)
    raw_data = crawl(spiders)
    os.chdir(original_cwd)
    process_data(raw_data)


if __name__ == '__main__':
    main()
