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
    # TODO: process data
    pass


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
