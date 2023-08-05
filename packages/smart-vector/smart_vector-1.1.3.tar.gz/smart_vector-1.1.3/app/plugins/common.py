import json
from django.conf import settings as dj_settings
from smart_vector import SmartVectorDB

try:
    from yaml import CLoader as Loader, CDumper as Dumper, load, dump
except ImportError:
    from yaml import Loader, Dumper, load, dump


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def object_hook(dict1):
    for key, value in dict1.items():
        if isinstance(value, dict):
            dict1[key] = dotdict(value)
        else:
            dict1[key] = value
    return dotdict(dict1)


# color print
def get_color(color):
    colorDict = {
        'green': "\033[1;32m",
        'red': "\033[1;31m",
        'white': "\033[1;37m"
    }
    return colorDict.get(color, '')


def error_print(*s):
    print(get_color('red'), end="")
    print(*s)
    print(get_color('white'), end="")


def success_print(*s):
    print(get_color('green'), end="")
    print(*s)
    print(get_color('white'), end="")


def get_setting():
    stream = open(getattr(dj_settings, 'WENDA_CONFIG', 'config.yml'), encoding='utf8')
    # current_path = os.path.dirname(os.path.abspath(__file__))
    # stream = open(os.path.join(current_path, '../../config.yml'), encoding='utf8')
    settings = load(stream, Loader=Loader)
    settings = dotdict(settings)
    stream.close()
    try:
        settings.llm = settings.llm_models[settings.llm_type]
    except:
        print("没有读取到LLM参数，可能是因为当前模型为API调用。")
    del settings.llm_models

    # 生产环境不打印敏感数据
    # import re
    # settings_str_toprint = dump(dict(settings))
    # settings_str_toprint = re.sub(r':', ":" + "\033[1;32m", settings_str_toprint)
    # settings_str_toprint = re.sub(r'\n', "\n\033[1;31m", settings_str_toprint)
    # print("\033[1;31m", end="")
    # print(settings_str_toprint, end="")
    # print("\033[1;37m")

    return json.loads(json.dumps(settings), object_hook=object_hook)


settings = get_setting()

# Vector Settings
if dj_settings.TEXT_VEC_API:
    from smart_vector import Text2VecAPIFunction

    text2vec = Text2VecAPIFunction(
        appid=settings.text2vec_api.appid, token=settings.text2vec_api.token, url=settings.text2vec_api.url)
else:
    from smart_vector import Text2VecEmbeddingFunction
    text2vec = Text2VecEmbeddingFunction()


connect_dict = {
    'host': settings.smart_database.host,
    'port': settings.smart_database.port,
    'user': settings.smart_database.username,
    'password': settings.smart_database.password,
    'db': settings.smart_database.db
}
smart_database = SmartVectorDB(db_config=connect_dict, load_host=settings.smart_database.load_host,
                               text_vector=text2vec)


import threading


class CounterLock:
    def __init__(self):
        self.lock = threading.Lock()
        self.waiting_threads = 0
        self.waiting_threads_lock = threading.Lock()

    def acquire(self):
        with self.waiting_threads_lock:
            self.waiting_threads += 1
        acquired = self.lock.acquire()

    def release(self):
        self.lock.release()
        with self.waiting_threads_lock:
            self.waiting_threads -= 1

    def get_waiting_threads(self):
        with self.waiting_threads_lock:
            return self.waiting_threads

    def __enter__(self):  # 实现 __enter__() 方法，用于在 with 语句的开始获取锁
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):  # 实现 __exit__() 方法，用于在 with 语句的结束释放锁
        self.release()
