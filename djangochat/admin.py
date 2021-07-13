from django.contrib import admin
from django.db.models.aggregates import Count
from .models import User, Chatbot, Chats
from django.core.paginator import Paginator
from django.db import models
from django.core.cache import cache
# from django.core.pagination import Paginato
 
class ChatbotAdmin(admin.ModelAdmin):
    list_display= ["id", "title"]
    search_fields= ["id", "title"]
    list_display= ["id", ]

    class Meta:
        model = Chatbot
 
# Register your models here.
admin.site.register(User)
admin.site.register(Chatbot, ChatbotAdmin)

class CachingPaginator(Paginator):
    def __get__count(self):
        if not hasattr(self, "_count"):
            self._count= None

        if self._count is None:
            try:
                key = "adm:{0}:count".format(hash(self.object_list.query.__str__())) 
                self._count= cache.get(key, -1)
                if self._count== -1:
                    self._count=super().count
                    cache.set(key, self._count, 3600)

            except:
                self._count = len(self.object_list)
        return self._count
    count= property(__get__count)


class ChatsAdmin(admin.ModelAdmin):
    list_filter = ['room', 'user', 'time']
    list_display= ['room', 'user', 'time', 'content']
    search_fields = ['room__title', 'user__username', 'content']
    list_display= ['room', 'user', 'time']
    readonly_fields=['id', 'room', 'user', 'time']

    show_full_result_count= False
    paginator =CachingPaginator

    class Meta:
        model = Chats

admin.site.register(Chats, ChatsAdmin)


