from django.contrib import admin
from .models import (Movie,Cast,Torrent,Magnet,WebTor,Embed,Download,Comment,StaticTag,Term,
DynamicTag)
class AdminMovie(admin.ModelAdmin):
    search_fields=["title","category"]
    list_display = ["title","category"]
class AdminCast(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["name"]
#for torrent and magent model
class AdminTor(admin.ModelAdmin):
    search_fields = ["movie__title"]
    list_display = ["movie"]
class AdminComment(admin.ModelAdmin):
    search_fields = ["comment","movie__title","user__username"]
    list_display = ["comment","movie","user"]
class AdminSaticTag(admin.ModelAdmin):
    search_fields = ["tag","portion"]
    list_display = ["tag","portion"]
class AdminDynamicTag(admin.ModelAdmin):
    search_fields = ["movie","tag","portion"]
    list_display = ["movie","tag","portion"]
class AdminTerm(admin.ModelAdmin):
    search_fields = ["paragraph","created_on"]
    list_display = ["paragraph"]
admin.site.register(StaticTag,AdminSaticTag)
admin.site.register(DynamicTag,AdminDynamicTag)
admin.site.register(Term,AdminTerm)
admin.site.register([Torrent,Magnet,WebTor,Embed,Download],AdminTor)
admin.site.register(Comment,AdminComment)
admin.site.register(Cast,AdminCast)
admin.site.register(Movie,AdminMovie)
