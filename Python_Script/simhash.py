# -*-coding:utf-8-*-
from __future__ import division,unicode_literals

import re
import sys
import hashlib
import collections
import numbers

from itertools import groupby

if sys.version_info[0]>=3:
    basestring=str
    unicode=str
    long=int
else:
    basestring=bytes
    unicode=unicode
    long=long
    range=xrange

def _hashfunc(x):
    return int(hashlib.md5(x).hexdigest(),16)

class Simhash(object):
    __slots__=['value','f','reg','hashfunc']

    def __init__(self,value,f=64,reg=r'[\w\u4e00-\u9fcc]+',hashfunc=None):
        self.f=f
        self.reg=reg
        self.value=None

        if hashfunc:
            self.hashfunc=hashfunc
        else:
            self.hashfunc=_hashfunc 
        
        if isinstance(value,Simhash):
            self.value=value.value
        elif isinstance(value,basestring):
            self.build_weight_by_text(unicode(value))
        elif isinstance(value,collections.Iterable):
            self.build_hash_by_features(value)
        elif isinstance(value,numbers.Integral):
            self.value=value
        else:
            raise Exception('Bad parameter with type {}'.format(type(value)))
        
    def __eq__(self,other):
        return self.value==other.value
    
    def _side(self,content,width=2):
        return [content[i:i+width] for i in range(max(len(content)-width+1,1))]

    def _tokenize(self,content):
        content=content.lower()
        content=''.join(re.findall(self.reg,content))
        ans=self._side(content)
        return ans
    
    def build_weight_by_text(self,content):
        features=self._tokenize(content)
        features={k:sum(1 for _ in g) for k,g in groupby(sorted(features))}
        return self.build_hash_by_features(features)
    
    def build_hash_by_features(self,features):
        v=[0]*self.f
        maskes=[1<<i for i in range(self.f)]

        if isinstance(features,dict):
            features=features.items()
        for f in features:
            if isinstance(f,basestring):
                h=self.hashfunc(f.encode('utf-8'))
                w=1
            else:
                assert isinstance(f,collections.Iterable)
                h=self.hashfunc(f[0].encode('utf-8'))
                w=f[1]
            for i in range(self.f):
                v[i]+= w if h & maskes[i] else -w
        ans =0
        for i in range(self.f):
            if v[i]>0:
                ans |=maskes[i]
        self.value =ans
    def distance(self,another):
        assert self.f==another.f 
        x=(self.value^another.value) &((1<<self.f)-1)
        ans =0 
        while x:
            ans +=1
            x &=x-1
        return ans


class SimhashIndex(object):
    def __init__(self,objs,f=64,k=3):
        """
        objs=[[id,simhash]]
        """
        self.k=k
        self.f=f
        
        self.bucket=collections.defaultdict(set)

        for i,q in enumerate(objs):
            self.add(*q)
        
    def add(self,obj_id,simhash):
        assert simhash.f==self.f

        for key in self.get_keys(simhash):
            v= '%x,%s' % (simhash.value,obj_id)
            self.bucket[key].add(v)

    def delete(self,obj_id,simhash):
        assert simhash.f==self.f

        for key in self.get_keys(simhash):
            v='%x,%s'%(simhash.value,obj_id)
            if key in self.bucket:
                self.bucket[key].remove(v)
    
    def get_near_dump(self,simhash):
        assert simhash.f==self.f

        ans=set()
        for key in self.get_keys(simhash):
            dups=self.bucket[key]

            for dup in dups:
                sim2,obj_id=dup.split(',',1)
                sim2=Simhash(long(sim2,16),self.f)
                d=simhash.distance(sim2)
                if d<=self.k:
                    ans.add(obj_id)
        return list(ans)

    @property
    def offsets(self):
        return [self.f//(self.k+1)*i for i in range(self.k+1)]

    def get_keys(self,simhash):
        for i ,offset in enumerate(self.offsets):
            if i==(len(self.offsets)-1):
                m=2**(self.f-offset)-1
            else:
                m=2**(self.offsets[i+1]-offset)-1
            c=simhash.value>>offset&m
            yield '%x:%x' % (c,i)
if __name__ == "__main__":
    import pandas as pd 
    sim1=Simhash(value='佛山优化公司 http://www.soyikj.com ■既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？ 美国特斯拉上海工厂、德国巴斯夫广东湛江项目；美国埃克森美孚惠州项目、韩国三星电子西安高新区项目、荷兰锂能沃克斯公司浙江绿色储能锂电池项目……这是近段时间以来选择落户中国的大型外资项目。国家发改委有关负责人日前表示，中国将继续促进外商投资便利化，还会有第三批重大外资项目。 近年来，对于中国投资环境的讨论，甚至“外资撤离论”等论调不时被热炒。但一笔笔大型外资项目、真金白银的投入和近年来保持较快增长的新设外资企业数量，是对真实情况最好的说明——外商来中国投资，正是好时候。 何以见得？对许多外商投资者和投资机构来说，投资最重要的影响因素无外乎两点，一是市场潜力，一是营商环境。在这两方面，中国都已展现良好的基础和极具吸引力的未来。 看市场潜力，中国经济是一片大海。近14亿人口的消费大市场，4亿人左右的中等收入群体，预计未来15年将分别进口商品和服务超过30万亿美元和10万亿美元，这是中国市场的庞大体量。消费升级的趋势正火热上演，新型城镇化和区域协调发展正让广袤的乡村和欠发达地区面貌日新月异。层次丰富，需求各异，这是中国市场的多元结构。今年以来，减税降费、促进形成强大国内市场等一系列措施还在不断出台，让消费者更有能力、有意愿消费，这是中国市场可期的未来。 看营商环境，中国的提升有目共睹。从审批变注册备案、越来越薄的负面清单到“多证合一”、等待时间大幅缩短，这些经营过程中的实际体验，企业感受最明显。在世界银行发布的《2019年营商环境报告》中，中国营商环境较2017年大幅上升32位，位列全球第46名。中国美国商会发布的2019年《中国商务环境调查报告》也显示，中国积极的国内消费市场前景以及逐步改善的营商环境，使中国继续成为全球投资的首选目的地。 这些外部评价背后，是中国一以贯之改善营商环境的努力。全国两会期间表决通过的《外商投资法》，更是将这种决心和行动以法的形式推向高潮。法治是最好的营商环境。有了法律规定，便是全国一盘棋，不管走到哪里，外商投资有法可依、有法必依。当然，法律出台还只是第一步，后续实施落地还有相当多的工作要做，还需要许多有关部门的配合、协调，但是未来的道路是明确的，方向是坚定的，更加公正、透明、可预期的营商环境将在法律的权威保障下日益成为现实。 既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？（肖麦） （本文来自于新华网）')
    sim2=Simhash(value='■既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？ 美国特斯拉上海工厂、德国巴斯夫广东湛江项目；美国埃克森美孚惠州项目、韩国三星电子西安高新区项目、荷兰锂能沃克斯公司浙江绿色储能锂电池项目……这是近段时间以来选择落户中国的大型外资项目。国家发改委有关负责人日前表示，中国将继续促进外商投资便利化，还会有第三批重大外资项目。 近年来，对于中国投资环境的讨论，甚至“外资撤离论”等论调不时被热炒。但一笔笔大型外资项目、真金白银的投入和近年来保持较快增长的新设外资企业数量，是对真实情况最好的说明——外商来中国投资，正是好时候。 何以见得？对许多外商投资者和投资机构来说，投资最重要的影响因素无外乎两点，一是市场潜力，一是营商环境。在这两方面，中国都已展现良好的基础和极具吸引力的未来。 看市场潜力，中国经济是一片大海。近14亿人口的消费大市场，4亿人左右的中等收入群体，预计未来15年将分别进口商品和服务超过30万亿美元和10万亿美元，这是中国市场的庞大体量。消费升级的趋势正火热上演，新型城镇化和区域协调发展正让广袤的乡村和欠发达地区面貌日新月异。层次丰富，需求各异，这是中国市场的多元结构。今年以来，减税降费、促进形成强大国内市场等一系列措施还在不断出台，让消费者更有能力、有意愿消费，这是中国市场可期的未来。 看营商环境，中国的提升有目共睹。从审批变注册备案、越来越薄的负面清单到“多证合一”、等待时间大幅缩短，这些经营过程中的实际体验，企业感受最明显。在世界银行发布的《2019年营商环境报告》中，中国营商环境较2017年大幅上升32位，位列全球第46名。中国美国商会发布的2019年《中国商务环境调查报告》也显示，中国积极的国内消费市场前景以及逐步改善的营商环境，使中国继续成为全球投资的首选目的地。 这些外部评价背后，是中国一以贯之改善营商环境的努力。全国两会期间表决通过的《外商投资法》，更是将这种决心和行动以法的形式推向高潮。法治是最好的营商环境。有了法律规定，便是全国一盘棋，不管走到哪里，外商投资有法可依、有法必依。当然，法律出台还只是第一步，后续实施落地还有相当多的工作要做，还需要许多有关部门的配合、协调，但是未来的道路是明确的，方向是坚定的，更加公正、透明、可预期的营商环境将在法律的权威保障下日益成为现实。 既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？')
    sim3=Simhash(value='蓝洁瑛资料来中国投资，拥抱开放新机遇（开放谈） ■既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？ 美国特斯拉上海工厂、德国巴斯夫广东湛江项目；美国埃克森美孚惠州项目、韩国三星电子西安高新区项目、荷兰锂能沃克斯公司浙江绿色储能锂电池项目……这是近段时间以来选择落户中国的大型外资项目。国家发改委有关负责人日前表示，中国将继续促进外商投资便利化，还会有第三批重大外资项目。 近年来，对于中国投资环境的讨论，甚至“外资撤离论”等论调不时被热炒。但一笔笔大型外资项目、真金白银的投入和近年来保持较快增长的新设外资企业数量，是对真实情况最好的说明——外商来中国投资，正是好时候。 何以见得？对许多外商投资者和投资机构来说，投资最重要的影响因素无外乎两点，一是市场潜力，一是营商环境。在这两方面，中国都已展现良好的基础和极具吸引力的未来。 看市场潜力，中国经济是一片大海。近14亿人口的消费大市场，4亿人左右的中等收入群体，预计未来15年将分别进口商品和服务超过30万亿美元和10万亿美元，这是中国市场的庞大体量。消费升级的趋势正火热上演，新型城镇化和区域协调发展正让广袤的乡村和欠发达地区面貌日新月异。层次丰富，需求各异，这是中国市场的多元结构。今年以来，减税降费、促进形成强大国内市场等一系列措施还在不断出台，让消费者更有能力、有意愿消费，这是中国市场可期的未来。 看营商环境，中国的提升有目共睹。从审批变注册备案、越来越薄的负面清单到“多证合一”、等待时间大幅缩短，这些经营过程中的实际体验，企业感受最明显。在世界银行发布的《2019年营商环境报告》中，中国营商环境较2017年大幅上升32位，位列全球第46名。中国美国商会发布的2019年《中国商务环境调查报告》也显示，中国积极的国内消费市场前景以及逐步改善的营商环境，使中国继续成为全球投资的首选目的地。 这些外部评价背后，是中国一以贯之改善营商环境的努力。全国两会期间表决通过的《外商投资法》，更是将这种决心和行动以法的形式推向高潮。法治是最好的营商环境。有了法律规定，便是全国一盘棋，不管走到哪里，外商投资有法可依、有法必依。当然，法律出台还只是第一步，后续实施落地还有相当多的工作要做，还需要许多有关部门的配合、协调，但是未来的道路是明确的，方向是坚定的，更加公正、透明、可预期的营商环境将在法律的权威保障下日益成为现实。 既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？ (责编：刘晓琰(实习生)、樊海旭)')
    sim4=Simhash(value='原标题：来中国投资，拥抱开放新机遇(开放谈) 既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？ 美国特斯拉上海工厂、德国巴斯夫广东湛江项目；美国埃克森美孚惠州项目、韩国三星电子西安高新区项目、荷兰锂能沃克斯公司浙江绿色储能锂电池项目……这是近段时间以来选择落户中国的大型外资项目。国家发改委有关负责人日前表示，中国将继续促进外商投资便利化，还会有第三批重大外资项目。 近年来，对于中国投资环境的讨论，甚至“外资撤离论”等论调不时被热炒。但一笔笔大型外资项目、真金白银的投入和近年来保持较快增长的新设外资企业数量，是对真实情况最好的说明——外商来中国投资，正是好时候。 何以见得？对许多外商投资者和投资机构来说，投资最重要的影响因素无外乎两点，一是市场潜力，一是营商环境。在这两方面，中国都已展现良好的基础和极具吸引力的未来。 看市场潜力，中国经济是一片大海。近14亿人口的消费大市场，4亿人左右的中等收入群体，预计未来15年将分别进口商品和服务超过30万亿美元和10万亿美元，这是中国市场的庞大体量。消费升级的趋势正火热上演，新型城镇化和区域协调发展正让广袤的乡村和欠发达地区面貌日新月异。层次丰富，需求各异，这是中国市场的多元结构。今年以来，减税降费、促进形成强大国内市场等一系列措施还在不断出台，让消费者更有能力、有意愿消费，这是中国市场可期的未来。 看营商环境，中国的提升有目共睹。从审批变注册备案、越来越薄的负面清单到“多证合一”、等待时间大幅缩短，这些经营过程中的实际体验，企业感受最明显。在世界银行发布的《2019年营商环境报告》中，中国营商环境较2017年大幅上升32位，位列全球第46名。中国美国商会发布的2019年《中国商务环境调查报告》也显示，中国积极的国内消费市场前景以及逐步改善的营商环境，使中国继续成为全球投资的首选目的地。 这些外部评价背后，是中国一以贯之改善营商环境的努力。全国两会期间表决通过的《外商投资法》，更是将这种决心和行动以法的形式推向高潮。法治是最好的营商环境。有了法律规定，便是全国一盘棋，不管走到哪里，外商投资有法可依、有法必依。当然，法律出台还只是第一步，后续实施落地还有相当多的工作要做，还需要许多有关部门的配合、协调，但是未来的道路是明确的，方向是坚定的，更加公正、透明、可预期的营商环境将在法律的权威保障下日益成为现实。 既有蒸蒸日上的营商环境，也有充分可能的市场空间，任何立足国际化的企业怎么可能不来拓展中国市场？ 最新网 www.zuinow.com 2019-03-26 09:24:26 营商 环境 中国 外资项目 市场')

    # df=pd.read_excel('xiangsi_.xlsx',encoding='utf-8')
    
    print(sim1.distance(sim2))
    print(sim1.distance(sim3))
    print(sim1.distance(sim4))
    print(sim2.distance(sim3))
    print(sim2.distance(sim4))
    print(sim3.distance(sim4))            