# -*- coding: utf-8 -*-
import os
import time
import scrapy

from souyun.items import SouyunItem


#./data/author/storyname/story|poetry
class StorySpider(scrapy.Spider):
    name = 'Story'
    allowed_domains = ['sou-yun.com']
    url='https://sou-yun.com/AllusionsIndex.aspx?sort=People&page='
    authorset=0         #人物页面URL
    Storyset=0          #典故页面URL
    start_urls =[url+str(authorset)]
    items=[]            #总数据集

    def parse(self, response):
        if self.authorset<12:
            for each in response.xpath('//div[@class="fullBlock"]/div[@class="inline1"]'):
                item={}
                item['Author']=each.xpath('./a/text()').extract()[0]
                item['AuthorUrl']="https://sou-yun.com"+str(each.xpath('./a/@href').extract()[0])
                item['AuthorCount']=each.xpath('./a/span/text()').extract()[0][2:-1]
                self.items.append(item)

            if self.authorset<11:
                self.authorset +=1
                yield scrapy.Request(self.url+str(self.authorset),callback=self.parse)
                return
        for item in self.items:
            itemFilename="./Data/" + item['Author']

            if not os.path.exists(itemFilename):
                os.makedirs(itemFilename)

            self.Storyset=0
            time.sleep(1)
            yield scrapy.Request(url=item['AuthorUrl'],meta={'meta_1':item},callback=self.story_parse)      


    #涉及人物递归解析（弃用？）
    def author_parse(self, response):
        for each in response.xpath('//div[@class="fullBlock"]/div[@class="inline1"]'):
            item={}
            item['Author']=each.xpath('./a/text()').extract()
            item['AuthorUrl']=each.xpath('./a/@href').extract()[0]
            item['AuthorCount']=each.xpath('./a/span/text()').extract()[0][2:-1]
            self.items.append(item)
            yield item
        if self.authorset<12:
            self.authorset +=1
            
        yield scrapy.Request(self.url+str(self.authorset),callback=self.author_parse)
    
    #典故出处解析
    def story_parse(self, response):
        meta_1=response.meta['meta_1']
        for each in response.xpath('//div[@id="IndexPanel"]/a'):
            item=SouyunItem()
            item['Author']=meta_1['Author']
            item['AuthorUrl']=meta_1['AuthorUrl']
            item['AuthorCount']=meta_1['AuthorCount']
            item['StoryName']=each.xpath('./text()').extract()[0]
            item['StoryNumber']=each.xpath('./@href').extract()[0][24:-2]
            
            item['Story']={}
            for stor in response.xpath('//div[@id="item_{}"]/div[2]/p'.format(item['StoryNumber'])):
                try:
                    strsname=str(stor.xpath('./span[@class="book"]/a/text()').extract()[0])
                except:
                    strsname=str(stor.xpath('./span[@class="book"]/text()').extract()[0])
                strs=str(stor.xpath('./span[@class="bookContent"]/text()').extract()[0])
                item['Story'][strsname]=strs

            item['Poetry']={}
            for stor in response.xpath('//div[@id="item_{}"]/div[last()]/p'.format(item['StoryNumber'])):
                strs=str(stor.xpath('./text()').extract()[0])
                strsname=str(stor.xpath('./span/text()').extract()[0])+str(stor.xpath('./span/a/text()').extract()[0])
                item['Poetry'][strsname]=strs

            yield item
            
        time.sleep(1)
        self.Storyset+=1
        yield scrapy.Request(url=item['AuthorUrl']+"&page="+str(self.Storyset),meta={'meta_1':item},callback=self.story_parse)
