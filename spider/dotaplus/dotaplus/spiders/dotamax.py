import scrapy
from data.cfg import DotamaxCfg
from data import CUSTOM_DATA
import copy


class NameDictSpider(scrapy.Spider):
    name = 'name_dict'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
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


class CNNameDictSpider(scrapy.Spider):
    name = 'cn_name_dict'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
        'FEED_FORMAT': 'json',
        'FEED_URI': 'cn_name_dict_raw.json',
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN'
        }
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
    name = 'win_rate'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
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
                'win_rate_all_all_all': float(_wr)
            }
        for server in DotamaxCfg.Server:
            for skill in DotamaxCfg.Skill:
                for ladder in DotamaxCfg.Ladder:
                    if server == skill == ladder == 'all':
                        continue
                    url = '/hero/rate/?server={}&skill={}&ladder={}'. \
                        format(server, skill, ladder)
                    request = response.follow(
                        url, callback=self.parse_other)
                    request.meta['cfg'] = '_'.join([server, skill, ladder])
                    yield request

    def parse_other(self, response):
        cfg = response.meta['cfg']
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
                'win_rate_' + cfg: float(_wr)
            }


class MatchUpsSpider(scrapy.Spider):
    name = 'match_ups'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
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
            for server in DotamaxCfg.Server[0:]:
                for skill in DotamaxCfg.Skill[0:]:
                    for ladder in DotamaxCfg.Ladder[0:]:
                        cfg_url = '?server={}&skill={}&ladder={}'. \
                            format(server, skill, ladder)
                        request = response.follow(
                            anti_url + cfg_url, callback=self.parse_matchups)
                        request.meta['hero_name'] = hero_name
                        request.meta['cfg'] = '_'.join([server, skill, ladder])
                        yield request

    def parse_matchups(self, response):
        hero_name = response.meta['hero_name']
        cfg = response.meta['cfg']
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
        hero_list = copy.deepcopy(CUSTOM_DATA['cn_layout'])
        match_ups = {}
        for idx, h in enumerate(anti_hero):
            anti_hero_name = h.replace('/hero/detail/', '')
            match_ups[anti_hero_name] = float(anti_index[idx].replace('%', ''))
            hero_list.remove(anti_hero_name)
        for hero in hero_list:
            match_ups[hero] = 0.0
        yield {
            'hero_name': hero_name,
            'match_ups_' + cfg: match_ups
        }


class TeammatesSpider(scrapy.Spider):
    name = 'teammates'
    allowed_domains = ['www.dotamax.com']
    start_urls = ['http://www.dotamax.com/hero/rate/']
    custom_settings = {
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
            for server in DotamaxCfg.Server[0:]:
                for skill in DotamaxCfg.Skill[0:]:
                    for ladder in DotamaxCfg.Ladder[0:]:
                        cfg_url = '?server={}&skill={}&ladder={}'. \
                            format(server, skill, ladder)
                        request = response.follow(
                            comb_url + cfg_url, callback=self.parse_teammates)
                        request.meta['hero_name'] = hero_name
                        request.meta['cfg'] = '_'.join([server, skill, ladder])
                        yield request

    def parse_teammates(self, response):
        hero_name = response.meta['hero_name']
        cfg = response.meta['cfg']
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
        hero_list = copy.deepcopy(CUSTOM_DATA['cn_layout'])
        teammates = {}
        for idx, h in enumerate(coop_hero):
            coop_hero_name = h.replace('/hero/detail/', '')
            teammates[coop_hero_name] = float(coop_index[idx].replace('%', ''))
            hero_list.remove(coop_hero_name)
        for hero in hero_list:
            teammates[hero] = 0.0
        yield {
            'hero_name': hero_name,
            'teammates_' + cfg: teammates
        }
