"""MoviesQuick URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views
from movies.sitemaps import MoviesViewSitemap
from .sitemaps import StaticViewSitemap
sitemaps = {
    "movies":MoviesViewSitemap,
    "static":StaticViewSitemap,
}
urlpatterns = [
    path('admin/', admin.site.urls),
    path("torrent/",include("torrents.urls",namespace="torrents")),
    path("sitemap.xml",views.index,{"sitemaps":sitemaps},name="django.contrib.sitemaps.views.sitemap"),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},name='django.contrib.sitemaps.views.sitemap'),
    path("",include("movies.urls",namespace="movies")),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
else:
    handler404 = "MoviesQuick.views.handle_page_not_found"
    handler500 = "MoviesQuick.views.handle_server_error"