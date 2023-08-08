from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from app.views import api_chat_stream, api_find, api_chat_box, api_find_dynamic, index, indexui
from app.zsk import api_read_news, api_save_news, api_sd_agent, api_find_rtst_in_memory

from app import master

urlpatterns = [
    path('', master.index),
    path('login/', master.login_view),
    path('wenda/', index),
    path('wendaui/', indexui),
    path('admin/', admin.site.urls),
    path('app/', include('app.urls')),
    path('api/chat_stream', api_chat_stream),
    path('api/find', api_find),
    path('api/find_dynamic', api_find_dynamic),
    path('chat/completions', api_chat_box),
    # zsk
    path('api/read_news', api_read_news),
    path('api/save_news', api_save_news),
    path('api/sd_agent', api_sd_agent),
    path('api/find_rtst_in_memory', api_find_rtst_in_memory),

    # smartchart
    path('echart/', include('smart_chart.echart.urls')),
]