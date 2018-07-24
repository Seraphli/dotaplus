from scrapy import cmdline
from util import get_path
import os
import json


def get_data():
    original_cwd = os.getcwd()
    project_path = get_path('scrapy/dotaplus')
    os.chdir(project_path)
    if os.path.exists('heroes_raw.json'):
        os.remove('heroes_raw.json')
    if os.path.exists('heroes.json'):
        os.remove('heroes.json')
    cmdline.execute('scrapy crawl dotamax --nolog -o heroes_raw.json'.split())
    with open('heroes_raw.json', 'r') as f:
        heroes_raw = json.load(f)
    heroes = {}
    for h in heroes_raw:
        hero_name = h['hero_name']
        heroes[hero_name] = {
            'real_name': h['hero_real_name'],
            'anti': h['anti']
        }
    os.chdir(original_cwd)


if __name__ == '__main__':
    get_data()
