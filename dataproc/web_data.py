import os


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

    def crawl_data(self):
        os.chdir(self.spider_path)
        self._crawl()
        raw_data = load_json(spider_names, file_names)
        os.chdir(self.original_cwd)

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
