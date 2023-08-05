

import requests
import json

from app.plugins.common import settings

# 能力类型
ability_type = "chatGLM"
# 引擎类型
engine_type = "chatGLM"
     

def chat_init(history):
    history_data = []
    if history is not None:
        history_data = []
        for i, old_chat in enumerate(history):
                history_data.append(old_chat['content'])
    return history_data


def chat_one(prompt, history_formatted, max_length, top_p, temperature, zhishiku=False):
    headers = {'Content-Type': 'application/json',
        "User-Agent": "python-requests/2.24.0", "Accept": "*/*"}
    data = {"query": prompt, "history": history_formatted}
    resp = requests.post(settings.chatglm_api.url, data=json.dumps(data), headers=headers, stream=True)
    try:
        for line in resp.iter_lines():
            if line in [b'', b'event: delta']:
                continue
            try:
                line = line.decode(encoding="utf-8")
                result = json.loads(line[5:])
                yield result['response']
            except Exception as e:
                yield ""
    except Exception as e:
        yield f"模型预测出现异常。异常问题：{e}" 


def load_model():
     pass


class Lock:
    def __init__(self):
        pass

    def get_waiting_threads(self):
        return 0

    def __enter__(self): 
        pass

    def __exit__(self, exc_type, exc_val, exc_tb): 
        pass