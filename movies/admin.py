from django.contrib import admin
from .models import Movie,Cast,Torrent,Magnet,WebTor,Embed,Download
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
admin.site.register([Torrent,Magnet,WebTor,Embed,Download],AdminTor)
admin.site.register(Cast,AdminCast)
admin.site.register(Movie,AdminMovie)
