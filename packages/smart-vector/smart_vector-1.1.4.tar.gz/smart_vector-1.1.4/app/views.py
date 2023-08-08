from django.http import StreamingHttpResponse, FileResponse, Http404, JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import datetime
import os
import logging
import re
import json
from app.plugins.common import error_print
from app.plugins.common import settings as wenda_settings
from app.models import ChatRecords

RomanNumeralsMap = {
    'III': 3,
    'II': 2,
    'IV': 4,
    'IX': 9,
    'XL': 40,
    'XC': 90,
    'CD': 400,
    'CM': 900,
    'I': 1,
    'V': 5,
    'X': 10,
    'L': 50,
    'C': 100,
    'D': 500,
    'M': 1000
}


def find_RomanNumerals(input_str):
    number = 0
    if input_str in RomanNumeralsMap:
        number += RomanNumeralsMap[input_str]
    return number


@login_required
def index(request):
    llm_type = wenda_settings.llm_type
    return render(request, 'wenda/index.html', {'llm_type': llm_type})


@login_required
def indexui(request):
    return render(request, 'wenda/indexui.html')


if settings.LOAD_LLM:
    # import torch
    from app.llm import mutex, zhishiku, LLM


    @csrf_exempt
    def api_find(request):
        if request.method == 'POST':
            data = json.loads(request.body.decode())
            prompt = data.get('prompt')
            step = data.get('step')
            collection = data.get('collection')
            if step is None:
                step = int(wenda_settings.library.step)
            return JsonResponse(zhishiku.find(prompt, int(step), request={'username':request.user.username,'collection':collection}), safe=False)


    @csrf_exempt
    def api_chat_stream(request):
        if not request.user.is_authenticated:
            return StreamingHttpResponse('auth fail')
        data = json.loads(request.body.decode())
        if not data:
            return StreamingHttpResponse('0')
        prompt = data.get('prompt')
        r_prompt = data.get('r_prompt', prompt)
        max_length = data.get('max_length', 2048)
        top_p = data.get('top_p', 0.7)
        temperature = data.get('temperature', 0.9)
        use_zhishiku = data.get('zhishiku', False)
        collection = data.get('collection')
        keyword = data.get('keyword', prompt)
        history = data.get('history')
        history_formatted = LLM.chat_init(history)  # make sure LLM is defined
        IP = request.META.get('REMOTE_ADDR')
        memory_name = request.user.username
        theme = data.get('theme', 'test')

        def stream():
            error = ""
            footer = '///'
            response = ''
            nonlocal use_zhishiku, prompt
            if use_zhishiku:
                response_d = zhishiku.find(keyword, int(wenda_settings.library.step),
                                           request={'username': memory_name, 'collection': collection})
                if len(response_d) == 0:
                    use_zhishiku = False
                    prompt = 'system: 请扮演一名专业分析师，根据以下内容回答问题：' + prompt + "\n"
                    if wenda_settings.library.show_soucre == True:
                        footer = "\n### 未查找到资料///"
                else:
                    output_sources = [i['title'] for i in response_d]
                    results = '\n'.join([str(i + 1) + ". " + re.sub('\n\n', '\n',
                                                                    response_d[i]['content']) for i in
                                         range(len(response_d))])
                    prompt = 'system: 请扮演一名专业分析师，根据以下内容回答问题：' + prompt + "\n" + results
                    if wenda_settings.library.show_soucre == True:
                        footer = "\n### 来源：\n" + ('\n').join(output_sources) + '///'
            with mutex:
                print("\033[1;32m" + IP + ":\033[1;31m" + prompt + "\033[1;37m")
                try:
                    for response in LLM.chat_one(prompt, history_formatted, max_length, top_p, temperature,
                                                 zhishiku=use_zhishiku):
                        if response:
                            yield response + footer
                except Exception as e:
                    error = str(e)
                    import traceback
                    traceback.print_exc(e)
                    error_print("错误", error)
                    response = ''
                    # torch.cuda.empty_cache()
            if response == '':
                yield "发生错误，正在重新加载模型" + error + '///'
                # os._exit(0)
            ChatRecords.objects.create(user=memory_name, theme=theme, question=r_prompt, answer=response, ip=IP)
            yield "/././"

        return StreamingHttpResponse(stream())


    @csrf_exempt
    def api_chat_stream_new(request):
        if not request.user.is_authenticated:
            return StreamingHttpResponse('auth fail')
        data = json.loads(request.body.decode())
        if not data:
            return StreamingHttpResponse('0')
        prompt = data.get('prompt')
        r_prompt = data.get('r_prompt', prompt)
        max_length = data.get('max_length', 2048)
        top_p = data.get('top_p', 0.7)
        temperature = data.get('temperature', 0.9)
        use_zhishiku = data.get('zhishiku', False)
        keyword = data.get('keyword', prompt)
        history = data.get('history')
        history_formatted = LLM.chat_init(history)  # make sure LLM is defined
        IP = request.META.get('REMOTE_ADDR')
        memory_name = request.user.username
        theme = data.get('theme', 'test')

        specific_prompts = wenda_settings.prompts.Title2Paper.prompt
        is_paper = wenda_settings.prompts.Title2Paper.is_paper
        outline = wenda_settings.prompts.Title2Paper.outline

        pre_responce = ""

        def stream(use_zhishiku, prompt):
            error = ""
            footer = '///'
            response = ''
            nonlocal pre_responce
            if use_zhishiku:
                response_d = zhishiku.find(keyword, int(wenda_settings.library.step), memory_name=memory_name)
                if len(response_d) == 0:
                    prompt = prompt + "\n"
                    if wenda_settings.library.show_soucre == True:
                        footer = "\n### 未查找到资料///"
                else:
                    output_sources = [i['title'] for i in response_d]
                    results = '\n'.join([str(i + 1) + ". " + re.sub('\n\n', '\n',
                                                                    response_d[i]['content']) for i in
                                         range(len(response_d))])
                    prompt = prompt + "\n" + results
                    if wenda_settings.library.show_soucre == True:
                        footer = "\n### 来源：\n" + ('\n').join(output_sources) + '///'
            with mutex:
                print("\033[1;32m" + IP + ":\033[1;31m" + prompt + "\033[1;37m")
                try:
                    for response in LLM.chat_one(prompt, history_formatted, max_length, top_p, temperature,
                                                 zhishiku=use_zhishiku):
                        if response:
                            yield pre_responce + "\n" + response + footer
                    pre_responce = pre_responce + "\n" + response
                except Exception as e:
                    error = str(e)
                    error_print("错误", error)
                    response = ''
                    # torch.cuda.empty_cache()
            if response == '':
                yield "发生错误，正在重新加载模型" + error + '///'
            ChatRecords.objects.create(user=memory_name, theme=theme, question=prompt, answer=response, ip=IP)
            yield "/././"

        def loop_stream():
            pre_prompt = 'system: 请扮演一名专业分析师，根据以下内容回答问题：'
            nonlocal pre_responce
            if is_paper:
                if outline:
                    prompts = list(map(lambda x: x.split('.', 1)[-1], specific_prompts[-1].split("\n")))
                    for prompt_i in prompts:
                        prompt_in = pre_prompt + "\n" + specific_prompts[-1].format(title=r_prompt) + "\n" + prompt_i
                        yield from stream(use_zhishiku, prompt_in)
                else:
                    prompt_in = pre_prompt + "\n" + specific_prompts[0] + "\n" + r_prompt
                    for responce in LLM.chat_one(prompt_in, history_formatted, max_length, top_p, temperature,
                                                 zhishiku=use_zhishiku):
                        yield pre_prompt + "\n" + responce
                    pre_prompt += "\n" + responce
                    ChatRecords.objects.create(user=memory_name, theme=theme, question=prompt_in, answer=responce,
                                               ip=IP)
                    prompts = responce.replace('/\n- /g', '\n1.').split("\n")
                    for line in prompts:
                        if not line.strip() or len(line.split(".", 1)) < 2:
                            continue
                        line = line.split(".", 1)
                        num = find_RomanNumerals(line[0])
                        prompt_in = pre_prompt + "\n" + specific_prompts[-1].format(title=r_prompt) + "\n" + line[-1]
                        yield from stream(use_zhishiku, prompt_in)
            else:
                pre_prompt = 'system: 请扮演一名专业分析师，根据以下内容回答问题：'
                prompt_in = pre_prompt + "\n" + r_prompt
                yield from stream(use_zhishiku, prompt_in)

        return StreamingHttpResponse(loop_stream())


    @csrf_exempt
    def api_chat_box(request):
        if request.method == 'OPTIONS':
            # handle OPTIONS request here
            response = StreamingHttpResponse()
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Headers'] = 'content-type'
            return response

        elif request.method == 'POST':
            data = json.loads(request.body.decode())
            # rest of your logic here...
            max_length = data.get('max_tokens')
            if max_length is None:
                max_length = 2048
            top_p = data.get('top_p')
            if top_p is None:
                top_p = 0.2
            temperature = data.get('temperature')
            if temperature is None:
                temperature = 0.8
            use_zhishiku = data.get('zhishiku')
            if use_zhishiku is None:
                use_zhishiku = False
            messages = data.get('messages')
            prompt = messages[-1]['content']
            # print(messages)
            history_formatted = LLM.chat_init(messages)
            response_text = ''
            # print(request.environ)
            IP = request.environ.get('HTTP_X_REAL_IP') or request.environ.get('REMOTE_ADDR')
            error = ""

            def event_stream():
                response_text = ''
                # this mutex should be defined elsewhere
                with mutex:
                    try:
                        for response_text in LLM.chat_one(prompt, history_formatted, max_length, top_p, temperature,
                                                          zhishiku=use_zhishiku):
                            if response_text:
                                yield f"data: {json.dumps({'response': response_text})}\n\n"

                        yield "data: %s\n\n" % "[DONE]"
                    except Exception as e:
                        error = str(e)
                        response_text = ''
                        # torch.cuda.empty_cache()
                    if response_text == '':
                        yield "data: %s\n\n" % json.dumps({"response": ("发生错误，正在重新加载模型" + error)})

            response = StreamingHttpResponse(event_stream())
            response['Content-Type'] = 'text/event-stream'
            response['Cache-Control'] = 'no-cache'
            response['Connection'] = 'keep-alive'
            return response


    # 根据前端需求动态查找知识库相关信息
    # s=要查询的内容
    # step=分多少步查询
    # count=知识抽取的数量
    # paraJson=参数包，以json字符串的形式编写
    # 知识库配置模式，冒号前面是知识库类别，后面是拟抽取的数量，示例 paraJson.libraryStategy:"bing:2 bingsite:3 fess:2 rtst:3 sogowx:2"
    # 知识库最大抽取条目的数量，paraJson.maxItmes
    @csrf_exempt
    def api_find_dynamic(request):
        data = json.loads(request.body.decode())
        if not data:
            return '0'
        prompt = data.get('prompt')
        step = data.get('step')
        paraJson = data.get('paraJson')  # 转成json对象

        if step is None:
            step = int(wenda_settings.library.step)

        if paraJson is None:
            paraJson = {
                'libraryStategy': "sogowx:2 bingsite:3 fess:2 rtst:3 bing:2", 'maxItmes': 10}

        print(type(paraJson))
        print(paraJson)
        return JsonResponse(zhishiku.find_dynamic(prompt, int(step), paraJson), safe=False)
else:
    from app.llms import llm_chatglm as LLM


    @csrf_exempt
    def api_find(request):
        if request.method == 'POST':
            return JsonResponse([{'title': 'smartchart', 'content': 'good tools'}], safe=False)


    @csrf_exempt
    def api_chat_stream(request):
        if not request.user.is_authenticated:
            return StreamingHttpResponse('auth fail')
        data = json.loads(request.body.decode())
        if not data:
            return StreamingHttpResponse('0')
        prompt = data.get('prompt')
        r_prompt = data.get('r_prompt', prompt)
        max_length = data.get('max_length', 2048)
        top_p = data.get('top_p', 0.7)
        temperature = data.get('temperature', 0.9)
        use_zhishiku = data.get('zhishiku', False)
        keyword = data.get('keyword', prompt)
        history = data.get('history')
        history_formatted = LLM.chat_init(history)  # make sure LLM is defined
        IP = request.META.get('REMOTE_ADDR')
        memory_name = request.user.username
        theme = data.get('theme', 'test')

        def stream():
            error = ""
            footer = '///'
            response = ''
            print("\033[1;32m" + IP + ":\033[1;31m" + prompt + "\033[1;37m")
            try:
                for response in LLM.chat_one(prompt, history_formatted, max_length, top_p, temperature,
                                             zhishiku=use_zhishiku):
                    if response:
                        yield response + footer
            except Exception as e:
                error = str(e)
                error_print("错误", error)
                response = ''
            if response == '':
                yield "发生错误，正在重新加载模型" + error + '///'
                # os._exit(0)
            print(response)
            ChatRecords.objects.create(user=memory_name, theme=theme, question=r_prompt, answer=response, ip=IP)
            yield "/././"

        return StreamingHttpResponse(stream())


    def api_chat_box(request):
        pass


    def api_find_dynamic(request):
        pass
