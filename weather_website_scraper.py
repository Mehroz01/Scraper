import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import Crawler
from scrapy.settings import Settings
from scrapy import log
import re
import flask
from flask import request, jsonify



class Jokes_SPider(scrapy.Spider):
    name="jokes"

    weather={}


    def __init__(self, start_urls=None, *args, **kwargs):
        if start_urls is not None:

            self._start_urls = start_urls
            print(self._start_urls)
        # else:
        #     self._start_urls = []
        super(Jokes_SPider, self).__init__(*args, **kwargs)

    def start_requests(self):
        start_url=['https://www.accuweather.com/en/us/bullhead-city-az/86429/current-weather/2123777']
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse)



    ###############################50 percent work ##############################################################


    def parse(self, response):

        for quote in response.xpath("//div[@id='details']/div"):
            #print(quote)

            self.weather['temperature']=quote.xpath("div/div/div[@class='info']/div[@class='temp']/span/text()").extract_first()

            self.weather['wind_speed'] =quote.xpath("div/div[@class='more-info']/ul/li[2]//strong/text()").extract_first()
            self.weather['Humidity'] =quote.xpath("div/div[@class='more-info']/ul/li[3]//strong/text()").extract_first()
            self.weather['pressure_mb'] =quote.xpath("div/div[@class='more-info']/ul/li[4]//strong/text()").extract_first()
            self.weather['Cloud_cover'] =quote.xpath("div/div[@class='more-info']/ul/li[6]//strong/text()").extract_first()
            print('temperature is ',int(re.search(r'\d+', self.weather['temperature']).group()))
            print('wind_speed is ', int(re.search(r'\d+', self.weather['wind_speed']).group()))
            print('pressure_mb is ', float(re.search(r'\d+', self.weather['pressure_mb']).group()))
            print('Humidity is ', int(re.search(r'\d+', self.weather['Humidity']).group()))

        ac=response.xpath("//div[@id='details']/ul/li[2]")
        a1=ac.xpath("a/@href").extract_first()
        print('\n ***********************anchor is ****************************** \n ',a1)
        print('anchor type is ',type(a1))
        print('########################### 2nd Scrapy Request ###################################################')



        start_url = [a1]
        for url in start_url:
            yield scrapy.Request(url=url, callback=self.parse_2)

    def parse_2(self,response):



        for quote in response.xpath("//div[@id='details']/div/div"):#//div[@id='feed-tabs']#//div[@id='details']/div/div[@class='day muted']
            self.weather['Gusts']=quote.xpath("div/div[2]/div/div/ul/li[3]/strong/text()").extract_first()
            self.weather['Precipitation']=quote.xpath("div/div[2]/ul/li[3]/strong/text()").extract_first()

        print('###############################################################################################')
        print(self.weather)
        print('###############################################################################################')


# def scrp():

# for i in range(0,2):
#     print('scrap is calling')
#
#     process = CrawlerProcess({
#         #'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
#     })
#
#     process.crawl(Jokes_SPider)
#     process.start()
    #


import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor


def run_spider():
    def f(q):
        try:

            runner = crawler.CrawlerRunner()
            spider = Jokes_SPider(start_urls='test')#pass parameter here
            deferred = runner.crawl(spider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()




app = flask.Flask(__name__)

@app.route('/service/start', methods=['POST'])
def build():
    run_spider()


    return jsonify('done')



if __name__ == '__main__':


    app.run(debug=False, port='3030', host='0.0.0.0')


