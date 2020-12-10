from django.shortcuts import render
from .models import Movie
from django.views.generic import (ListView,
DetailView,
)
class MovieHome(ListView):
    model = Movie
    template_name="movies/home.html"
    context_object_name="movies"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent"] = Movie.objects.order_by("-uploaded_on")[0:8]
        context["featured"] = Movie.objects.filter(status__contains="featured").order_by("-uploaded_on")[:8]
        context["mostwatched"] = Movie.objects.filter(status__contains="mostwacthed").order_by("-uploaded_on")[:8]
        return context
class MovieDetail(DetailView):
    model = Movie
    template_name = 'movies/detail.html'
    context_object_name = "movie"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views +=1
        self.object.save(update_fields=["views",])
        return context
    