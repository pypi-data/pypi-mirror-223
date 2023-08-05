import requests
import re
session = requests.Session()
# 正则提取摘要和链接
title_pattern = re.compile('id="sogou_vr_11002601_title_\d" uigs="article_title_\d">(.*?)</a>')
brief_pattern = re.compile('<p class="txt-info".+">(.*?)</p>')
link_pattern = re.compile('<a target="_blank" href="(.+)" id="')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'}
proxies = {"http": None,"https": None,}


def find(search_query,step = 0):
    url = 'https://weixin.sogou.com/weixin?ie=utf8&s_from=input&_sug_=y&_sug_type_=&type=2&query={}'.format(search_query)
    res = session.get(url, headers=headers, proxies=proxies)
    r = res.text

    title = title_pattern.findall(r)
    brief = brief_pattern.findall(r)
    link = link_pattern.findall(r)

    # 数据清洗
    clear_brief = []
    for i in brief:
        tmp = re.sub('<[^<]+?>', '', i).replace('\n', '').strip()
        tmp1 = re.sub('^.*&ensp;', '', tmp).replace('\n', '').strip()
        tmp2 = re.sub('^.*>', '', tmp1).replace('\n', '').strip()
        clear_brief.append(tmp2)

    clear_title = []
    for i in title:
        tmp = re.sub('^.*?>', '', i).replace('\n', '').strip()
        tmp2 = re.sub('<[^<]+?>', '', tmp).replace('\n', '').strip()
        clear_title.append(tmp2)
    return [{'title': "["+clear_title[i]+"]("+"https://weixin.sogou.com"+link[i]+")", 'content':clear_brief[i]}
            for i in range( len(brief))]


