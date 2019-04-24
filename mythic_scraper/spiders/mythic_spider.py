import scrapy


class MythicSpider(scrapy.Spider):
    name = "mythic"

    def start_requests(self):
        urls = [
            'http://mythicspoiler.com/war/cards/gideonblackblade.html'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print_formatted_card(response)
        pass


def print_formatted_card(response):
    print(get_card_title(response))
    print(get_card_cost(response))
    print(get_card_type(response))
    print(get_card_text(response))
    print('\n _______________________________________________________________________________________________________ \n')


def get_card_title(response):
    return response.xpath('normalize-space(//td[@colspan="2" and @valign="top"])').get().strip()


def get_card_type(response):
    return response.xpath('normalize-space(//table[@valign="top" and @align="center"]/tr[3]/td)').get().strip()


def get_card_text(response):
    return response.xpath('string(//table[@valign="top" and @align="center"]/tr[4]/td)').get().strip()


def get_card_cost(response):
    return response.xpath('//td[@colspan="2" and @valign="top"]/text()').getall()[1].strip()
