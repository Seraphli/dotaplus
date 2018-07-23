from scrapy import cmdline
from util import get_path
import os

project_path = get_path('scrapy/dotaplus')
os.chdir(project_path)
cmdline.execute('scrapy crawl dotamax --nolog -o heroes.json'.split())
