from scrapy import Spider, Request 
from stockx.items import StockxItem
from datetime import datetime
import re
import time

#USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"


class StockXspider(Spider):
    name = 'nike_spider'
    allowed_domains = ['stockx.com']
    start_urls = ['https://stockx.com/nike?page=1']
    handle_httpstatus_list = [403]


    def parse(self, response):
        page_urls = ['https://stockx.com/nike?page={}'.format(x) for x in range(1,26)]

        for page_url in page_urls:
            #print(page_url)
            #time.sleep(30)
            yield Request(url=page_url, callback=self.parse_result_page, dont_filter = True)



    def parse_result_page (self, response):
        product_urls = response.xpath('//div[@class="tile Tile-c8u7wn-0 bCufAv"]/a/@href').extract()      
        product_urls = ['https://stockx.com' + url for url in product_urls]


        #print('='*55)
        #print(len(product_urls))
        #print('='*55)

        for url in product_urls:
            #print(url)
            #time.sleep(30)
            yield Request(url=url, callback=self.parse_product_page ,dont_filter = True)

    def parse_product_page(self, response):

        #extract product title
        product_title = response.xpath('//h1[@class="name"]/text()').extract_first()

        #extract lowest ask price 

        #extract highest bid price 

        try:
            lowest_ask, highest_bid = response.xpath('//div[contains(@class, "en-us stat-value")]/text()').extract()[0:2]
        except:
            print(f'Error unpacking lowest_ask and others at url: {response.url}')

        try:
            lowest_ask = float(lowest_ask.replace('$','').replace(',',''))
        except:
            lowest_ask = None

        try:
            highest_bid =float(highest_bid.replace('$','').replace(',',''))
        except:
            highest_bid = None


        #extract retail price
        try:
            retail_price = response.xpath('//span[@data-testid="product-detail-retail price"]/text()').extract_first()
            retail_price = float(retail_price.replace('$','').replace(',',''))

        except:
            retail_price = None


        #extract release date
        try:
            release_date = response.xpath('//span[@data-testid="product-detail-release date"]/text()').extract_first()
            #release_date = datetime.strptime(release_date, '%m/%d/%Y').date()
            #print release_date

        except:
            release_date = None
        
        try:
            style = response.xpath('//span[@data-testid="product-detail-style"]/text()').extract_first()

        except: 
            style = None

        #extract color
        try:
            color = response.xpath('//span[@data-testid="product-detail-colorway"]/text()').extract_first()
        except:
            color = None

        #extract voatility
        try:
            volatility = response.xpath('//span[@class="value"]/text()').extract()[2]
            volatility = float(volatility.replace('%',''))

        except:
            volatility = None


        try:
            number_of_sales, price_premium, avg_sale_price = response.xpath('//div[contains(@class, "gauge-value")]/text()').extract()

        except:
            print(f'Error unpacking num_sales and others at url: {response.url}')
        
        try:
            number_of_sales = float(number_of_sales.replace(',',''))
        except:
            number_of_sales = None
        try:
            price_premium = float(price_premium.replace('%',''))
        except:
            price_premium = None
        try:
            avg_sale_price = float(avg_sale_price.replace('$','').replace(',',''))
        except:
            avg_sale_price = None

        #extract number of sales
        #try:
            #number_of_sales = response.xpath('//div[@class="gauge-value"]/text()').extract()[0]
            #number_of_sales = float(number_of_sales)

        #except:
            #number_of_sales = None
        
        #extract price premium
        #try:
            #price_premium =response.xpath('//div[@class="gauge-value"]/text()').extract()[1]
                
            #if price_premium:
                #price_premium = float(price_premium.replace('%',''))
            
            #else: 
               # price_premium =response.xpath('//div[@class="gauge-value-negative"]/text()').extract()
                #price_premium = float(price_premium.replace('%',''))

        #except:
            #price_premium = None
        

        #extract average sale price 
        #try:
            #avg_sale_price = response.xpath('//div[@class="gauge-value"]/text()').extract()[2]
            #avg_sale_price = float(avg_sale_price.replace('$',''))

        #except:
            #avg_sale_price = None
        
        
        item = StockxItem()
        item['product_title'] = product_title
        item['lowest_ask'] = lowest_ask
        item['highest_bid'] = highest_bid
        item['retail_price'] = retail_price
        item['release_date'] = release_date
        item['style'] = style
        item['color'] = color
        item['volatility'] = volatility
        item['number_of_sales'] = number_of_sales
        item['price_premium'] = price_premium
        item['avg_sale_price'] = avg_sale_price

        yield item



        #meta= {'product_title': product_title,
            #'lowest_ask': lowest_ask, 
            #'highest_bid': highest_bid, 
            #'retail_price' : retail_price,
            #'release_date': release_date,
            #'color': color,
            #'volatility': volatility,
            #'number_of_sales': number_of_sales,
            #'price_premium': price_premium,
            #'avg_sale_price': avg_sale_price}

       
        #print('='*55)
        #print(meta)
        #print('='*55)




    #def 

        #for product_url in product_urls:
           #print(product_url)

         #for product_url in product_urls:
            #yield Request(url=product_url, callback=self.parse_product_page)


        #for product_url in product_urls:
            #print(product_url)



