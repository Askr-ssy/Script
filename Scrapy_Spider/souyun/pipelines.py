# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import time
import os

class SouyunPipeline(object):
    def process_item(self, item, spider):
        # with open()
        filepath='./data/'+str(item['Author'])+'/'+str(item['StoryName'])

        if(not os.path.exists(filepath)):
                os.makedirs(filepath)

        for k,v in item['Story'].items():
            with open(filepath+'/'+k+'.txt','w',encoding='utf-8') as file:
                file.write(v)
        with open(filepath+'/Poetry.txt','w',encoding='utf-8') as file:        
            for k,v in item['Poetry'].items():
                file.write(k+':'+v+'\n')
        return item
