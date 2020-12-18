from django.contrib.sitemaps import Sitemap
from django.urls import reverse
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq="monthly"
    protocol = "https"
    def items(self):
        return ["app_movies:movies_home","app_movies:contact","app_movies:terms","app_torrents:torrents_home"]
    def location(self,item):
        return reverse(item)