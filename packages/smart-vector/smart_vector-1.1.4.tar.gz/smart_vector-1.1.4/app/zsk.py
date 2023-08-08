from django.http import JsonResponse, HttpResponse
from django.conf import settings
from app.plugins.common import settings as cm_settings
from django.views.decorators.csrf import csrf_exempt
import re
import json
import requests

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36 Edg/94.0.992.31'}
proxies = {"http": None, "https": None, }


@csrf_exempt
def api_sd_agent(request):
    url = cm_settings.stablediffusion_api.url
    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=json.loads(request.body), proxies=proxies)
    r = response.text
    return HttpResponse(r)


# from langchain.docstore.document import Document
# from langchain.text_splitter import CharacterTextSplitter

# @csrf_exempt
# def api_upload_rtst_zhishiku(request):
#     from app.plugins.zhishiku_rtst import FAISS, embeddings, get_vectorstore, vectorstores
#     memory_name = request.user.username
#     try:
#         data = json.loads(request.body.decode())
#         title = data.get("title")
#         data = re.sub(r'！', "！\n", data.get("txt"))
#         data = re.sub(r'。', "。\n", data)
#         data = re.sub(r'[\n\r]+', "\n", data)
#         docs = [Document(page_content=data, metadata={"source": title})]

#         text_splitter = CharacterTextSplitter(
#             chunk_size=20, chunk_overlap=0, separator='\n')
#         doc_texts = text_splitter.split_documents(docs)

#         texts = [d.page_content for d in doc_texts]
#         metadatas = [d.metadata for d in doc_texts]
#         vectorstore_new = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
#         vectorstore = get_vectorstore(memory_name)
#         if vectorstore is None:
#             vectorstores[memory_name] = vectorstore_new
#         else:
#             vectorstores[memory_name].merge_from(vectorstore_new)
#         return HttpResponse('成功')
#     except Exception as e:
#         return HttpResponse(str(e))

# @csrf_exempt
# def api_save_rtst_zhishiku(request):
#     from app.plugins.zhishiku_rtst import vectorstores
#     memory_name = request.user.username
#     try:
#         data = json.loads(request.body.decode())
# vectorstores[memory_name].save_local('memory/' + memory_name)
#         return HttpResponse("保存成功")
#     except Exception as e:
#         return HttpResponse(str(e))


@csrf_exempt
def api_find_rtst_in_memory(request):
    from app.plugins.zhishiku_rtst import find
    data = json.loads(request.body.decode())
    prompt = data.get('prompt')
    step = data.get('step')
    collection = data.get('collection')
    if step is None:
        step = int(settings.library.step)
    return JsonResponse(find(prompt, int(step), request={'username': request.user.username, 'collection': collection}),
                        safe=False)


@csrf_exempt
def api_save_news(request):
    try:
        data = json.loads(request.body.decode())
        if not data:
            return HttpResponse('no data')
        title = data.get('title')
        txt = data.get('txt')
        cut_file = f"txt/{title}.txt"
        with open(cut_file, 'w', encoding='utf-8') as f:
            f.write(txt)
        return HttpResponse('success')
    except Exception as e:
        return HttpResponse(str(e))


@csrf_exempt
def api_read_news(request):
    # 获取真实地址
    try:
        data = json.loads(request.body.decode())
        url = data.get("url")
        r = session.get(url, headers=headers, proxies=proxies)
        url = ''.join(re.findall("url.+'(.*?)'", r.text))
    except:
        return "读取真实URL失败"
    if url == '':
        return "读取真实URL失败"
    # 读取公众号内容
    try:
        from bs4 import BeautifulSoup
        r = session.get(url, headers=headers, proxies=proxies)
        soup = BeautifulSoup(r.text, 'html.parser')
        text = str(soup.find(class_='rich_media_wrp'))
        text = re.sub(r'[\r\n]', '', text)
        text = re.sub(r'<script.+/script>', '', text)
        text = re.sub(r'(<[^>]+>|\s)', '', text)
        return HttpResponse(text)
    except:
        return HttpResponse("读取公众号失败")
