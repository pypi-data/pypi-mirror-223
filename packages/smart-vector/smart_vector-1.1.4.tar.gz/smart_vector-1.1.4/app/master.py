from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.conf import settings
from app.models import ChatRecords, Collections
import os
import json

from app.plugins.gen_data_st import Doc2Embbeding


@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'app/login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'app/login.html')


def index(request):
    if request.user.is_authenticated:
        return render(request, 'echart/index.html')
    else:
        return redirect('/admin/login/?next=/')


@login_required
def upload_files(request):
    return render(request, 'app/upload_files.html')


@csrf_exempt
def upload_file(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')  # 获取文件列表
        username = request.user.username
        file_path = os.path.join(settings.UPLOAD_PATH, 'memory', username)
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        for file in files:
            # if not file.name.endswith('.jpg') and not file.name.endswith('.png'):
            #     return JsonResponse({'message': 'Invalid file format'})
            # if file.size > 500000:
            #     return JsonResponse({'message': 'File too large'})
            filename = os.path.join(file_path, file.name)
            with open(filename, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
        return JsonResponse({'message': 'File uploaded successfully'})
    else:
        return JsonResponse({'message': 'Invalid request'})


@csrf_exempt
def update_model(request):
    if request.method == 'POST':
        username = request.user.username
        collection = request.POST.get('collection', "none")
        file_path = os.path.join(settings.UPLOAD_PATH, 'memory', username)
        if not os.path.exists(file_path):
            msg = "There are no files in the folder"
        else:
            Doc2Embbeding(collection=collection).run(vectorstore_dir=file_path)
            msg = 'Successfully updated model'
        return JsonResponse({'message': msg})
    else:
        return JsonResponse({'message': 'Invalid request'})

@csrf_exempt
def chat_history(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        theme = data.get('theme', 'test')
        username = request.user.username
        chatList = ChatRecords.objects.filter(is_delete=False, user=username, theme=theme)
        chatJson = []
        if chatList:
            for chat in chatList[:10]:
                chatJson = [{'role': 'user', 'content': chat.question, 'messageId': f'U{chat.id}',
                             'time': chat.create_time},
                            {'role': 'AI', 'content': chat.answer, 'messageId': f'A{chat.id}',
                             'time': chat.create_time}] + chatJson
        else:
            chatJson = [
                {'role': 'AI', 'content': '我是您的AI助手, 请向我提问吧', 'messageId': '1234455', 'time': '2023-01-02 12:00:00'}]

        return JsonResponse(chatJson, safe=False)


@csrf_exempt
def chat_historys(request):
    username = request.user.username
    chatList = ChatRecords.objects.filter(is_delete=False, user=username)
    conversationList = []
    messageList = []
    messageDict = {}
    if chatList:
        activeConversationId = chatList[0].theme

        for chat in chatList[:10]:
            message = [
                {'role': 'user', 'content': chat.question, 'messageId': f'U{chat.id}', 'time': chat.create_time},
                {'role': 'AI', 'content': chat.answer, 'messageId': f'A{chat.id}', 'time': chat.create_time}]
            if chat.theme in messageDict.keys():
                messageDict[chat.theme]['history'] = message + messageDict[chat.theme]['history']
            else:
                messageDict[chat.theme] = {
                    "conversationId": chat.theme,
                    "history": message
                }
        for k, v in messageDict.items():
            messageList.append(v)
            conversationList.append({
                "conversationId": k,
                "title": v['history'][0]['content'][:30],
                "time": v['history'][0]['time'],
                "msgCount": len(v['history'])
            })
        chatJson = {
            "activeConversationId": activeConversationId,
            "inputMessage": "",
            "finallyPrompt": "",
            "isSending": False,
            "isAbort": False,
            "conversationList": conversationList,
            "messageList": messageList,
            "temperature": 0.9,
            "max_length": 2048,
            "top_p": 0.3,
            "zhishiku": True,
            "promptTemplate": "system: 请扮演一名专业分析师，根据以下内容用中文回答问题：{{问题}}\n。如果您认为给出的内容和问题无关或没有提出问题，请忽略该数据内容再用中文回答。{{知识库}}"
        }
    else:
        chatJson = None

    return JsonResponse(chatJson, safe=False)


@csrf_exempt
def delete_conversation(request):
    username = request.user.username
    data = json.loads(request.body.decode())
    theme = data.get('theme')
    if theme:
        ChatRecords.objects.filter(theme=theme, user=username).delete()
    return JsonResponse({"msg": 'deleted'})



def chatui(request):
    return render(request, 'app/chat.html')


def chatui_ask(request):
    print(request.method)
    print(request.GET)
    message = {
        "type": 'text',
        "content": {
            "text": '智能助理进入对话，为您服务'
        }
    }
    return JsonResponse(message)


# ----------------  知识库管理 ---------------------
def get_collections(request):
    user = request.user
    collectionList = Collections.objects.filter(is_delete=False, users__exact=user.id)

