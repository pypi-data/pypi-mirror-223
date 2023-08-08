from django.urls import path
from app import master


urlpatterns = [
    path('upload_files/', master.upload_files, name='upload_files'),
    path('upload_file/', master.upload_file, name='upload_file'),
    path('chat_history/', master.chat_history, name='chat_history'),
    path('chat_historys/', master.chat_historys, name='chat_historys'),
    path('delete_conversation/', master.delete_conversation, name='delete_conversation'),
    path('chatui_ask/', master.chatui_ask, name='chatui_ask'),
    path('chatui/', master.chatui, name='chatui'),
    path('update_model/', master.update_model, name='modelupdate')
]
