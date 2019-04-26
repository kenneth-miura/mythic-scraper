import scrapy


class MythicSpider(scrapy.Spider):
    name = "mythic"
    url_starter = "http://mythicspoiler.com/"

    def start_requests(self):
        urls = [
            self.url_starter + 'newspoilers.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for href in get_daily_spoilers(response):
            yield scrapy.Request(url=self.url_starter + href, callback=self.parse_card)

    def parse_card(self, response):
        print_formatted_card(response)
        pass


def print_formatted_card(response):
    print(get_card_title(response))
    print(get_card_cost(response))
    print(get_card_type(response))
    print(get_card_text(response))
    print('\n ______________________________________________________________ \n')


def get_card_title(response):
    return response.xpath('normalize-space(//td[@colspan="2" and @valign="top"])').get().strip()


def get_card_type(response):
    return response.xpath('normalize-space(//table[@valign="top" and @align="center"]/tr[3]/td)').get().strip()


def get_card_text(response):
    return response.xpath('string(//table[@valign="top" and @align="center"]/tr[4]/td)').get().strip()


def get_card_cost(response):
    return response.xpath('//td[@colspan="2" and @valign="top"]/text()').getall()[1].strip()


def get_daily_spoilers(response):
    return response.xpath(
        '//tr[count(preceding-sibling::tr[contains(comment()[2], "DATE BREAKER")])=1]/td/a[contains(@href, "html")]/@href').getall()
