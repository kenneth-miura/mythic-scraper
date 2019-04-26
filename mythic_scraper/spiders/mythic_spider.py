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

    power_toughness_or_loyalty = get_card_power_toughness_or_loyalty(response)
    if power_toughness_or_loyalty is not None:
        print(power_toughness_or_loyalty)

    card_flavor_text = get_card_flavor_text(response)
    if card_flavor_text is not None:
        print(get_card_flavor_text(response))

    print('\n ______________________________________________________________ \n')


def get_card_title(response):
    return response.xpath('normalize-space(//td[@colspan="2" and @valign="top"])').get().strip()


def get_card_type(response):
    return response.xpath('normalize-space(//table[@valign="top" and @align="center"]/tr[3]/td)').get().strip()


def get_card_text(response):
    return response.xpath('string(//table[@valign="top" and @align="center"]/tr[4]/td)').get().strip()


def get_card_cost(response):
    return response.xpath('//td[@colspan="2" and @valign="top"]/text()').getall()[1].strip()


# Note: If the card is a planeswalker, this function returns the loyalty
def get_card_power_toughness_or_loyalty(response):
    # TODO: Implement some workaround so I don't add whitespace by printing nothing if card has no p/t
    return response.xpath('normalize-space(//td/font[contains(comment(), "P/T")]/text()[2])').get()


def get_card_flavor_text(response):
    # TODO: Implement some workaround so I don't add whitespace by printing nothing if card has no flavor text
    response.xpath(
        'normalize-space(//tr/td/i[contains(comment(), "FLAVOR TEXT")]/text()[2])').get()


def get_daily_spoilers(response):
    return response.xpath(
        '//tr[count(preceding-sibling::tr[contains(comment()[2], "DATE BREAKER")])=1]/td/a[contains(@href, "html")]/@href').getall()
