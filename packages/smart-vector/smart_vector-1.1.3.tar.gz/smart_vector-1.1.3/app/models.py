from django.db import models
from django.utils.safestring import mark_safe
from django.conf import settings


# Create your models here.
class ChatRecords(models.Model):
    user = models.CharField(max_length=50, verbose_name='用户名')
    theme = models.CharField(max_length=255, blank=True, null=True, verbose_name='备注')
    question = models.TextField(max_length=5000, blank=True, null=True, verbose_name='问题')
    answer = models.TextField(max_length=5000, blank=True, null=True, verbose_name='回答')
    ip = models.CharField(max_length=50, blank=True, null=True, verbose_name='IP')
    is_delete = models.BooleanField(default=False, verbose_name='删除')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.user

    class Meta:
        ordering = ["-id"]
        verbose_name = "聊天记录"
        verbose_name_plural = "聊天记录"


class Collections(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='集合编码')
    name = models.CharField(max_length=50, unique=True, verbose_name='集合名称')
    remark = models.TextField(max_length=255, blank=True, null=True, verbose_name='备注',
                              help_text="备注或者where条件: collection='' and sr='' and document like '%' ")
    is_delete = models.BooleanField(default=False, verbose_name='删除')
    is_where = models.BooleanField(default=False, verbose_name='自定义')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='collection_user', verbose_name='授权用户',
                                   blank=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-id"]
        verbose_name = "知识集合"
        verbose_name_plural = "知识集合"


class Documents(models.Model):
    collection = models.ForeignKey(Collections, verbose_name='归属集合', on_delete=models.CASCADE, related_name='col_doc')
    sr = models.CharField(max_length=50, verbose_name='类别')
    c = models.CharField(max_length=50, verbose_name='类别2', null=True, blank=True)
    document = models.TextField(max_length=500, verbose_name='内容')
    m = models.TextField(max_length=500, verbose_name='元数据', null=True, blank=True)
    is_sync = models.BooleanField(default=False, verbose_name='同步')

    def __str__(self):
        return self.sr

    class Meta:
        ordering = ["-id"]
        verbose_name = "知识同步"
        verbose_name_plural = "知识同步"


class UserProfile(models.Model):
    fromUser = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='用户', on_delete=models.CASCADE)
    collection = models.ForeignKey(Collections, verbose_name='归属集合', on_delete=models.CASCADE, related_name='col_usr')

    def __str__(self):
        return self.fromUser.username

    class Meta:
        verbose_name = "用户配置"
        verbose_name_plural = "用户配置"
