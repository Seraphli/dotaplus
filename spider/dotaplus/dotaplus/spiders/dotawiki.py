import scrapy


class CountersSpider(scrapy.Spider):
    name = 'counters'
    allowed_domains = ['dota2.gamepedia.com']
    start_urls = ['https://dota2.gamepedia.com/Heroes']
    custom_settings = {
        'LOG_ENABLED': False,
        'FEED_FORMAT': 'json',
        'FEED_URI': 'counters_raw.json'
    }

    def parse(self, response):
        hero_href = []
        hero_name = []
        for i in [2, 4, 6]:
            hero_href.extend(response.css('#mw-content-text > '
                                          'table:nth-child(2) > '
                                          f'tr:nth-child({i}) > td > div > '
                                          'div > a::attr(href)').extract())
            hero_name.extend(response.css('#mw-content-text > '
                                          'table:nth-child(2) > '
                                          f'tr:nth-child({i}) > td > div > '
                                          'div > a::attr(title)').extract())
        for idx, h in enumerate(hero_href):
            url = h + '/Counters'
            request = response.follow(url, callback=self.parse_counters)
            request.meta['hero_name'] = hero_name[idx]
            yield request

    def parse_counters(self, response):
        hero_name = response.meta['hero_name']
        all_hero = response.css('#mw-content-text > span > b > '
                                'a::attr(title)').extract()
        split_hero = response.css('#mw-content-text > h2+div+span > b > '
                                  'a::attr(title)').extract()
        good_against = all_hero.index(split_hero[1])
        work_well = len(all_hero) - all_hero[::-1].index(split_hero[2]) - 1
        counters = {
            'bad_against': all_hero[:good_against],
            'good_against': all_hero[good_against:work_well],
            'work_well': all_hero[work_well:]
        }
        yield {
            'hero_name': hero_name,
            'counters': counters
        }
