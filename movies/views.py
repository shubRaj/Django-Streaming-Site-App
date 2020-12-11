from django.shortcuts import render
from .models import Movie,Cast
from django.http import HttpResponseNotModified
from django.views.generic import (ListView,
DetailView,
)
import random
class MovieHome(ListView):
    model = Movie
    template_name="movies/home.html"
    context_object_name="movies"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent"] = Movie.objects.order_by("-uploaded_on")[0:8]
        context["featured"] = Movie.objects.filter(status__icontains="featured").order_by("-uploaded_on")[:8]
        context["mostwatched"] = Movie.objects.filter(status__icontains="mostwatched").order_by("-uploaded_on")[:8]
        return context
class MovieDetail(DetailView):
    model = Movie
    template_name = 'movies/detail.html'
    context_object_name = "movie"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views +=1
        self.object.save(update_fields=["views",])
        context["related_movies"] = Movie.objects.filter(category__icontains=self.object.category).order_by("-uploaded_on")[:12]
        return context
class MovieList(ListView):
    model = Movie
    paginate_by = 40
    template_name="movies/list.html"
    context_object_name = "movies"
    def get_queryset(self):
        self.queryset = Movie.objects.order_by("-uploaded_on")
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.queryset:
            #here i used set to prevent duplicacy
            context["recommended"] = {random.choice(Movie.objects.all()) for _ in range(20)}
        return context
    
class Search(MovieList):
    def get(self,request,*args,**kwargs):
        self.query = self.request.GET.get("query")
        if not self.query:
            return HttpResponseNotModified()
        return super().get(request,*args,**kwargs)
    def get_queryset(self):
        objects = Movie.objects.filter(title__icontains=self.query)|Movie.objects.filter(category__icontains=self.query)|Movie.objects.filter(language__icontains=self.query).order_by("-uploaded_on")
        return objects
