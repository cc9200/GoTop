# -*- coding: utf-8 -*-

"""

    Baidu zhidao searcher

"""
import operator

import random
import requests
import jieba
Agents = (
    "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
    "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36"
)


def baidu_count(keyword, answers, timeout=2):
    """
    Count the answer number from first page of baidu search

    :param keyword:
    :param timeout:
    :return:
    """
    headers = {
        # "Cache-Control": "no-cache",
        "Host": "www.baidu.com",
        "User-Agent": random.choice(Agents)
    }
    params = {
        "wd": keyword.encode("gbk")
    }
    resp = requests.get("http://www.baidu.com/s", params=params, headers=headers, timeout=timeout)
    if not resp.ok:
        print("baidu search error")
        return {
            ans: 0
            for ans in answers
        }
    html=resp.text
    summary={}
    for ans in answers:
        num=html.count(ans)
        summary[ans]=num
        if num==0:
            ans_cut=list(jieba.cut(ans))
            ans_count=0
            for word in ans_cut:
                if len(word)==1:
                  ##ans_cut.remove(word)  ##删除标点符号
                    continue
                ans_count+=html.count(word)##对分词的结果分别统计词频
            summary[ans]=ans_count  ##得到选项的分词词频之和
        
    default = list(summary.values())[0]
    if all([value == default for value in summary.values()]):
        answer_firsts = {
            ans: html.index(ans)
            for ans in answers
        }
        sorted_li = sorted(answer_firsts.items(), key=operator.itemgetter(1), reverse=False)
        answer_li, index_li = zip(*sorted_li)
        return {
            a: b
            for a, b in zip(answer_li, reversed(index_li))
        }
    return summary
