from django.contrib import admin
from app import models


@admin.register(models.ChatRecords)
class ChatRecordsAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'question', 'answer', 'is_delete', 'create_time')
    list_filter = ['user', 'theme', 'is_delete']
    search_fields = ['question', 'answer']
    list_per_page = 50


@admin.register(models.Collections)
class CollectionsAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'remark', 'is_delete', 'is_where', 'create_time')
    search_fields = ['code', 'name', 'remark']
    filter_horizontal = ('users',)
    list_per_page = 100


@admin.register(models.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('fromUser', 'collection',)
    list_per_page = 100


@admin.register(models.Documents)
class DocumentsAdmin(admin.ModelAdmin):
    list_display = ('collection', 'sr', 'document', 'c', 'm', 'is_sync')
    list_filter = ['collection', 'sr', 'is_sync']
    readonly_fields = ('is_sync',)
    search_fields = ['document', ]
    list_per_page = 200
    actions = ['document_add', 'reset_sync']

    def document_add(self, request, queryset):
        from app.plugins.zhishiku_rtst import add
        collection = []
        sr = []
        document = []
        categorys = []
        answers = []
        ids = []
        for item in queryset:
            collection.append(item.collection.code)
            sr.append(item.sr)
            document.append(item.document)
            categorys.append(item.c if item.c else '')
            answers.append(item.m if item.m else '')
            ids.append(item.id)
        if document:
            add(collection, sr, document, ids=ids, categorys=categorys, answers=answers, owners=request.user.username)
            queryset.update(is_sync=True)
        self.message_user(request, f'已完成的同步{len(document)}/{len(queryset)}')

    document_add.short_description = "同步"
    document_add.confirm = '确认开始同步?'

    def reset_sync(self, request, queryset):
        from app.plugins.zhishiku_rtst import clear
        collection = queryset[0].collection.code
        clear(collection, request.user.username)
        queryset.update(is_sync=False)

    reset_sync.short_description = "清除集合"
    reset_sync.confirm = '确认开始当前所选集合?'
