from django.urls import re_path,path
from . import views
app_name="app_torrents"
urlpatterns = [
    re_path(r"search/",views.TorrentHome.as_view(),name="torrents_home"),
    re_path(r"^(?P<pk>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$",views.TorrentDetail.as_view(),name="torrent_detail"),
]
