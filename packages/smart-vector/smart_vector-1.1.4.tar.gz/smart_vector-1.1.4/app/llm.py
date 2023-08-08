
import threading
# import torch
from app.plugins.common import success_print
from app.plugins.common import CounterLock
from app.plugins.common import settings
import app.plugins.zhishiku as zhishiku

# -------------------   加载大模型 -----------------------
"""
LLM: 模型模块变量
model: 实例化模型变量
"""


def load_LLM():
    try:
        from importlib import import_module
        LLM = import_module('app.llms.llm_' + settings.llm_type)
        return LLM
    except Exception as e:
        print("LLM模型加载失败，请阅读说明：https://github.com/l15y/wenda", e)


LLM = load_LLM()

if not hasattr(LLM, "Lock"):
    mutex = CounterLock()
else:
    mutex = LLM.Lock()

model = None
tokenizer = None


def load_model():
    with mutex:
        LLM.load_model()
    # torch.cuda.empty_cache()
    success_print("模型加载完成")


thread_load_model = threading.Thread(target=load_model)
thread_load_model.start()
