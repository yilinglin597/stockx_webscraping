# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class StockxItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_title = scrapy.Field()
    lowest_ask = scrapy.Field()
    highest_bid = scrapy.Field()
    retail_price = scrapy.Field()
    release_date = scrapy.Field()
    style = scrapy.Field()
    color = scrapy.Field()
    volatility = scrapy.Field()
    number_of_sales = scrapy.Field()
    price_premium = scrapy.Field()
    avg_sale_price = scrapy.Field()

