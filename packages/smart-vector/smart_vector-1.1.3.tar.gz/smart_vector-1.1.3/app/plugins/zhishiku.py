
from app.plugins.common import settings
from app.plugins.common import error_print
zsk = []
try:
    input_list = settings.library.strategy.split(" ")
except:
    error_print("读取知识库参数失败，这可能是新版本知识库配置方式变化导致的，请参照配置文件进行修改。知识库仍将继续加载，并使用默认参数："+"sogowx:3 bingsite:2 rtst:2 agents:0")
    input_list = "sogowx:3 bingsite:2 rtst:2 agents:0".split(" ")
for item in input_list:
    item = item.split(":")
    from importlib import import_module
    try:
        zhishiku = import_module('app.plugins.zhishiku_'+item[0])
        if zhishiku is None:
            error_print("载入知识库失败", item[0])
        zsk.append({'zsk': zhishiku, "count": int(item[1]), 
        "is_rtst":True if item[0]=="rtst" else False})

    except Exception as e:
        print('app.plugins.zhishiku_'+item[0])


def find(s, step=0, **kwargs):
    result = []
    for item in zsk:
        if item['zsk'].__name__.split('.')[-1] in ('zhishiku_rtst',):
            result += item['zsk'].find(s, step, **kwargs)[:item['count']]
        else:
            result += item['zsk'].find(s, step)[:item['count']]
    return result[:int(settings.library.count)]

def find_dynamic(s, step=0, memory_name=None, paraJson={'libraryStategy': "bing:2 bingsite:3 fess:2 rtst:3 sogowx:2", 'maxItmes': 10}):
    zsk = []
    input_list = paraJson['libraryStategy'].split(" ")
    for item in input_list:
        item = item.split(":")
        from importlib import import_module
        zhishiku = import_module('app.plugins.zhishiku_'+item[0])
        if zhishiku is None:
            error_print("动态载入知识库失败", item[0])
        zsk.append({'zsk': zhishiku, "count": int(item[1]), 
        "is_rtst":True if item[0]=="rtst" else False})

    result = []
    for item in zsk:
        if memory_name != None and item['is_rtst']:
            result += item['zsk'].find(s, step, memory_name=memory_name)[:item['count']]
        else:
            result += item['zsk'].find(s, step)[:item['count']]
    return result[:paraJson["maxItmes"]]
