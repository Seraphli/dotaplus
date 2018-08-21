from util import get_path
import os
import json
import codecs
import copy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.dotaplus.dotaplus.spiders.dotamax import NameDictSpider, \
    CNNameDictSpider, WinRateSpider, MatchUpsSpider, TeammatesSpider
from spider.dotaplus.dotaplus.spiders.dotawiki import CountersSpider
from get_hero_role import insert_into_data


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


def generate_hero_py(raw_data):
    lines = ['class Heroes(object):\n']
    for nd in raw_data['name_dict']:
        real_name = nd['hero_real_name']
        name = real_name.replace(' ', '_').replace('\'', '').replace('-', '_')
        lines.append('    {} = "{}"\n'.format(name, nd['hero_name']))
    lines.append('\n\nclass CNHeroes(object):\n')
    for nd in raw_data['cn_name_dict']:
        real_name = nd['hero_real_name']
        lines.append('    {} = "{}"\n'.format(real_name, nd['hero_name']))
    with codecs.open('heroes.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)


def process_data(raw_data):
    data = {}
    name_dict = {}
    for nd in raw_data['name_dict']:
        data[nd['hero_name']] = {
            'name': nd['hero_real_name'],
        }
        name_dict[nd['hero_real_name']] = nd['hero_name']
    for nd in raw_data['cn_name_dict']:
        data[nd['hero_name']]['cn_name'] = nd['hero_real_name']
    for wr in raw_data['win_rate']:
        data[wr['hero_name']]['win_rate'] = wr['win_rate']
    for mu in raw_data['match_ups']:
        data[mu['hero_name']]['match_ups'] = mu['match_ups']
    for tm in raw_data['teammates']:
        data[tm['hero_name']]['teammates'] = tm['teammates']
    for counter in raw_data['counters']:
        h = name_dict[counter['hero_name']]
        _counter = {}
        for k in counter['counters']:
            _heroes = []
            for h_name in counter['counters'][k]:
                _heroes.append(name_dict[h_name])
            _counter[k] = _heroes
        data[h]['counters'] = _counter
    for h in data:
        data[h]['c_match_ups'] = copy.deepcopy(data[h]['match_ups'])
        for mu in data[h]['c_match_ups']:
            if mu in data[h]['counters']['good_against']:
                data[h]['c_match_ups'][mu] += 5.0
                data[h]['c_match_ups'][mu] = round(
                    data[h]['c_match_ups'][mu], 2)
            if mu in data[h]['counters']['bad_against']:
                data[h]['c_match_ups'][mu] -= 5.0
                data[h]['c_match_ups'][mu] = round(
                    data[h]['c_match_ups'][mu], 2)
        data[h]['c_teammates'] = copy.deepcopy(data[h]['teammates'])
        for tm in data[h]['c_teammates']:
            if tm in data[h]['counters']['work_well']:
                data[h]['c_teammates'][tm] += 5.0
                data[h]['c_teammates'][tm] = round(
                    data[h]['c_teammates'][tm], 2)
    with open('data.json', 'w') as f:
        json.dump(data, f)

    if False:
        generate_hero_py(raw_data)


def main():
    spiders = [NameDictSpider, CNNameDictSpider, WinRateSpider,
               MatchUpsSpider, TeammatesSpider, CountersSpider]
    original_cwd = os.getcwd()
    project_path = get_path('spider/dotaplus')
    os.chdir(project_path)
    raw_data = crawl(spiders)
    os.chdir(original_cwd)
    process_data(raw_data)
    insert_into_data()


if __name__ == '__main__':
    main()
