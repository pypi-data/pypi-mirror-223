import os
import openai
from app.plugins.common import settings


def chat_init(history):
    return history


def chat_one(prompt, history_formatted, max_length, top_p, temperature, zhishiku=False):
    history_data = [ {"role": "system", "content": "You are a helpful assistant."}]
    if history_formatted is not None:
        for i, old_chat in enumerate(history_formatted):
            if old_chat['role'] == "user":
                history_data.append(
                    {"role": "user", "content": old_chat['content']},)
            elif old_chat['role'] == "AI" or old_chat['role'] == 'assistant':
                history_data.append(
                    {"role": "assistant", "content": old_chat['content']},)
    history_data.append({"role": "user", "content": prompt},)
    response = openai.ChatCompletion.create(
        engine=settings.openai.model,
        messages=history_data,
        max_tokens=max_length,
        top_p=top_p,
        temperature=temperature,
        stream=True
    )
    resTemp=""
    for chunk in response:
        if chunk['choices'][0]["finish_reason"]!="stop":
            if hasattr(chunk['choices'][0]['delta'], 'content'):
                resTemp+=chunk['choices'][0]['delta']['content']
                yield resTemp

chatCompletion = None


def load_model():
    openai.api_key = settings.openai.api_key
    openai.api_base = settings.openai.api_base
    openai.api_type = "azure"
    openai.api_version = settings.openai.api_version



class Lock:
    def __init__(self):
        pass

    def get_waiting_threads(self):
        return 0

    def __enter__(self): 
        pass

    def __exit__(self, exc_type, exc_val, exc_tb): 
        pass