from django.contrib.sitemaps import Sitemap
from .models import Movie
from django.urls import reverse
class MoviesViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"
    limit=200
    def items(self):
        return Movie.objects.order_by("-uploaded_on")