import scrapy


class NameDictSpider(scrapy.Spider):
    name = 'namedict'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'name_dict_raw.json'
    }

    def parse(self, response):
        hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr::attr(onclick)').extract()
        hero_real_name = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(1) > span::text').extract()
        for idx, h in enumerate(hero):
            url = h.replace('DoNav(\'', '').replace('\')', '')
            hero_name = url.replace('/hero/detail/', '')
            yield {
                'hero_name': hero_name,
                'hero_real_name': hero_real_name[idx],
            }


class WinRateSpider(scrapy.Spider):
    name = 'winrate'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'win_rate_raw.json'
    }

    def parse(self, response):
        hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr::attr(onclick)').extract()
        win_rate = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td > '
            'div.segment.segment-green::attr(style)').extract()
        for idx, h in enumerate(hero):
            url = h.replace('DoNav(\'', '').replace('\')', '')
            hero_name = url.replace('/hero/detail/', '')
            _wr = win_rate[idx].replace('width:', '').replace('%;', '')
            yield {
                'hero_name': hero_name,
                'win_rate': float(_wr)
            }


class MatchUpsSpider(scrapy.Spider):
    name = 'matchups'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'match_ups_raw.json'
    }

    def parse(self, response):
        hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr::attr(onclick)').extract()
        for idx, h in enumerate(hero):
            url = h.replace('DoNav(\'', '').replace('\')', '')
            hero_name = url.replace('/hero/detail/', '')
            anti_url = '/hero/detail/match_up_anti/{}/'.format(hero_name)
            request = response.follow(anti_url, callback=self.parse_matchups)
            request.meta['hero_name'] = hero_name
            yield request

    def parse_matchups(self, response):
        hero_name = response.meta['hero_name']
        anti_index = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(2) > '
            'div:nth-child(1)::text').extract()
        anti_hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(1) > '
            'a::attr(href)').extract()
        match_ups = {}
        for idx, h in enumerate(anti_hero):
            anti_hero_name = h.replace('/hero/detail/', '')
            match_ups[anti_hero_name] = float(anti_index[idx].replace('%', ''))
        yield {
            'hero_name': hero_name,
            'match_ups': match_ups
        }


class TeammatesSpider(scrapy.Spider):
    name = 'teammates'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'teammates_raw.json'
    }

    def parse(self, response):
        hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr::attr(onclick)').extract()
        for idx, h in enumerate(hero):
            url = h.replace('DoNav(\'', '').replace('\')', '')
            hero_name = url.replace('/hero/detail/', '')
            comb_url = '/hero/detail/match_up_comb/{}/'.format(hero_name)
            request = response.follow(comb_url, callback=self.parse_teammates)
            request.meta['hero_name'] = hero_name
            yield request

    def parse_teammates(self, response):
        hero_name = response.meta['hero_name']
        coop_index = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(2) > '
            'div:nth-child(1)::text').extract()
        coop_hero = response.css(
            'body > div.maxtopbar > div.main-shadow-box > '
            'div.main-container > div.container.xuning-box > '
            'table > tbody > tr > td:nth-child(1) > '
            'a::attr(href)').extract()
        teammates = {}
        for idx, h in enumerate(coop_hero):
            coop_hero_name = h.replace('/hero/detail/', '')
            teammates[coop_hero_name] = float(coop_index[idx].replace('%', ''))
        yield {
            'hero_name': hero_name,
            'teammates': teammates
        }
