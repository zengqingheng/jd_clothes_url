# -*- coding: utf-8 -*-
import scrapy
import re
import requests
from jd_url.items import JdUrlItem
import logging
logging.basicConfig(filename='jdurl.log',filemode='w',level=logging.WARNING,datefmt='%m/%d/%Y %I:%M:%S %p')

class ClothesSpider(scrapy.Spider):
    name = 'clothes'
    allowed_domains = ['channel.jd.com', 'search.jd.com', 'coll.jd.com', 'list.jd.com']
    start_urls = ["https://channel.jd.com/accessories.html",'https://channel.jd.com/women.html',"https://channel.jd.com/men.html",
    "https://channel.jd.com/mensshoes.html","https://channel.jd.com/1318-2628.html","https://channel.jd.com/jewellery.html","https://channel.jd.com/yundong.html",
    "https://channel.jd.com/children.html","https://channel.jd.com/womensshoes.html","https://channel.jd.com/bag.html","https://channel.jd.com/luxury.html"]
    count = 1
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Connection': 'keep-alive',
        'Host': 'search.jd.com',
        'Referer': 'https://search.jd.com/Search?keyword=%E7%89%9B%E4%BB%94%E8%A3%A4%E7%94%B7&enc=utf-8&pvid=olt4tati.7ri5o7',
        'X-Requested-With': 'XMLHttpRequest'
    }
    items = JdUrlItem()
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url,self.parse)

    def parse(self, response):
        site = scrapy.Selector(response)
        currentUrl = response.url
        try:
            if currentUrl == 'https://channel.jd.com/men.html':
                keywordUrl = site.xpath('//dl/dd[@class="item-cont"]/ul[@class="item-list clearfix"]/li/a/@href').extract()
                # 将关键字url中相同的url过滤一遍，然后抓取是filter也会过滤一遍
                self.judgeRepeat(keywordUrl)  # 数组是在原处修改，所以不需要在定义变量进行接收
                for index, urlMen in enumerate(keywordUrl):
                    if urlMen[0:6] != 'https:':
                        urlMen = "https:" + urlMen
                        print('index:', index, "parseurl:", urlMen)
                    yield scrapy.Request(urlMen, self.parseKeyword)

            elif currentUrl == 'https://channel.jd.com/women.html':
                site = scrapy.Selector(response)
                hrefListWomen = site.xpath('//div[@class="women-type-con"]/descendant::a/@href').extract()
                self.judgeRepeat(hrefListWomen)
                for index, urlWomen in enumerate(hrefListWomen):
                    if urlWomen[0:6] != 'https:':
                        urlWomen = "https:" + urlWomen
                        print('index:', index, "parseurl:", urlWomen)
                    yield scrapy.Request(urlWomen, self.parseKeyword, )
            elif currentUrl == 'https://channel.jd.com/mensshoes.html':
                site = scrapy.Selector(response)
                hrefListMenShoes = site.xpath('//div[@class="man-floor160531-01"]/div/descendant::a/@href').extract()
                print(hrefListMenShoes)
                self.judgeRepeat(hrefListMenShoes)
                for index, urlMenshoe in enumerate(hrefListMenShoes):
                    if urlMenshoe[0:6] != "https:":
                        urlMenshoe = "https:" + urlMenshoe
                    print(index, ":", urlMenshoe)
                    yield scrapy.Request(urlMenshoe, self.parseKeyword, )

            elif currentUrl == 'https://channel.jd.com/1318-2628.html':
                site = scrapy.Selector(response)
               # print(response.text)
                hrefListOutDoors = site.xpath('//div[@id="storeCategorys"]/div/descendant::a/@href').extract()
                self.judgeRepeat(hrefListOutDoors)
                for index, urlOutDoor in enumerate(hrefListOutDoors):
                    if urlOutDoor[0:6] != "https:":
                        urlOutDoor = "https:" + urlOutDoor
                    print(index, ":", urlOutDoor)
                    yield scrapy.Request(urlOutDoor, self.parseKeyword, )

            elif currentUrl == 'https://channel.jd.com/jewellery.html':
                site = scrapy.Selector(response)
                hrefListJewellery = site.xpath('//div[@id="jewelleryCategorys"]/div/descendant::a/@href').extract()
                self.judgeRepeat(hrefListJewellery)
                for index, urlJewellery in enumerate(hrefListJewellery):
                    if urlJewellery[0:6] != "https:":
                        urlJewellery = "https:" + urlJewellery
                    print(index, ":", urlJewellery)
                    yield scrapy.Request(urlJewellery, self.parseKeyword, )

            elif currentUrl == 'https://channel.jd.com/bag.html':
                site = scrapy.Selector(response)
                hrefListBag = site.xpath('//div[@class="categorys-inner"]/div/descendant::a/@href').extract()
                print('hrefBag:',hrefListBag)
                self.judgeRepeat(hrefListBag)
                for index, urlBag in enumerate(hrefListBag):
                    if urlBag[0:6] != "https:":
                        urlBag = "https:" + urlBag
                    print(index, ":", urlBag)
                    yield scrapy.Request(urlBag, self.parseKeyword,)

            elif currentUrl == 'https://channel.jd.com/womensshoes.html':
                site = scrapy.Selector(response)
                hrefListWomenShoes = site.xpath('//div[@class="women-type-con"]/div/descendant::a/@href').extract()
                self.judgeRepeat(hrefListWomenShoes)
                for index, urlWomenShoes in enumerate(hrefListWomenShoes):
                    if urlWomenShoes[0:6] != "https:":
                        urlWomenShoes = "https:" + urlWomenShoes
                    print(index, ":", urlWomenShoes)
                    yield scrapy.Request(urlWomenShoes, self.parseKeyword)

            elif currentUrl == 'https://channel.jd.com/children.html':
                site = scrapy.Selector(response)
                hrefListChildren = site.xpath('//div[@class="floor-tz-category160408"]/ul/descendant::a/@href').extract()
                self.judgeRepeat(hrefListChildren)
                for index, urlChildren in enumerate(hrefListChildren):
                    if urlChildren[0:6] != "https:":
                        urlChildren = "https:" + urlChildren
                    print(index, ":", urlChildren)
                    yield scrapy.Request(urlChildren, self.parseKeyword)

            elif currentUrl == 'https://channel.jd.com/luxury.html':
                print(1111)
                print('luxury:',response.text)
                hrefListLuxury = re.findall(r"'(//list.jd.com.*?)'", response.text)
                #hrefListLuxury.extend(re.findall("'(//search.jd.com.*?)'", response.text))
                print('hrefListLuxury:',hrefListLuxury)
                self.judgeRepeat(hrefListLuxury)
                for index, urlLuxury in enumerate(hrefListLuxury):
                    urlLuxury = "https:" + urlLuxury
                    yield scrapy.Request(urlLuxury, self.parseKeyword)

            elif currentUrl == 'https://channel.jd.com/yundong.html':
                jsUrl = "https://storage.360buyimg.com/portalstatic/static/pc.config.1b8f70c3.js"
                res = requests.get(jsUrl)

                hrefListYundong = re.findall(r'".*?(list.jd.com.*?)"', res.text)
                #hrefListYundong.extend(re.findall('".*?(search.jd.com.*?)"', response.text))
                print('hrefListYundong:',hrefListYundong)
                self.judgeRepeat(hrefListYundong)
                for index, urlYundong in enumerate(hrefListYundong):
                    urlYundong = "https://" + urlYundong.replace('\\', '')
                    yield scrapy.Request(urlYundong, self.parseKeyword, )

            elif currentUrl == 'https://channel.jd.com/accessories.html':
                hrefListAccessories = re.findall(r'".*?(list.jd.com.*?)"', response.text)
                hrefListAccessories.extend(re.findall('".*?(search.jd.com.*?)"', response.text))
                self.judgeRepeat(hrefListAccessories)
                for index, urlAccessories in enumerate(hrefListAccessories):
                    urlAccessories = "https://" + urlAccessories.replace('\\', '')
                    yield scrapy.Request(urlAccessories, self.parseKeyword)

        except Exception as e:
            print(e)
            logging.warning(e,currentUrl)
    def parseKeyword(self,response):
        site = scrapy.Selector(response)
        pagecount=0
        try:
            pagecount= int(site.xpath('//span[@class="fp-text"]/i/text()').extract_first())
            currentKeyWord = re.search('keyword=(.*?)&enc',response.url).group(1)
            '''
                data-spu这个数据是获取另外30个商品url的关键参数，利用数组的形式传递下去
            '''
            for i in range(1,pagecount+1):
                pageUrl = "https://search.jd.com/Search?keyword="+currentKeyWord+"&enc=utf-8&page="+str(2*i-1)
                yield scrapy.Request(pageUrl,self.parseEveryPage)
        except AttributeError:
            for j in range(1,pagecount+1):
                otherPageUrl = response.url+"&page="+str(j)
                yield scrapy.Request(otherPageUrl,self.parseEveryPage)
        except TypeError:
            logging.warning("进入了不符合要求的页面")
            print("进入了不符合要求的页面")

    def parseEveryPage(self,response):
        site = scrapy.Selector(response)
        print('response.url:',response.url)
        #这个错误是在首页url并没有page这个字符串导致的，所以此时pageNumber=1
        try:
            pageNum = int(re.search('page=(.*)',response.url).group(1))
        except AttributeError:
            pageNum = 1
        goodsIdList = site.xpath('//ul[@class="gl-warp clearfix"]/li/@data-sku | //ul[@class="gl-warp clearfix"]/li/div/@data-sku').extract()
        print("goodsList:",goodsIdList)
        #在这里获取另外30个商品的数据，然后增加到goods List当中
        #因为是先获取前30个商品的信息之后，才能将下30个的信息获取，然后请求，再得到相应的数据
        data_pid = site.xpath('//ul[@class="gl-warp clearfix"]/li/@data-pid').extract()
        if data_pid != []:
            pidListStr = ','.join(data_pid)
            requestUrl = "https://search.jd.com/s_new.php?keyword=牛仔裤男&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&page="+str(pageNum+1)+"&s=140&scrolling=y&log_id=1533715932.74177&tpl=3_L&show_items="+pidListStr
            res =  requests.get(requestUrl,headers = self.headers,verify=False)
            site = scrapy.Selector(res)
            secondGoodsIdList = site.xpath('//li[@class="gl-item"]/@data-sku').extract()
            goodsIdList.extend(secondGoodsIdList)
            print("length:",len(goodsIdList))
            for id in goodsIdList:
                goodsUrl ='https://item.jd.com/'+id+'.html'
                print(self.count,goodsUrl)
                self.items['urlCount']=self.count
                self.items['url'] = goodsUrl
                self.count+=1
                yield self.items
        else:
            print("当前数据是一次性加载成功的，不需要二次请求")
            for id in goodsIdList:
                goodsUrl = 'https://item.jd.com/' + id + '1.html'
                print(self.count, goodsUrl)
                self.items['urlCount'] = self.count
                self.items['url'] = goodsUrl
                self.count += 1
                yield self.items

    def judgeRepeat(self,judgeList):
        for url in judgeList:
            for index in range(judgeList.count(url)-1):
                judgeList.remove(url)
        return judgeList