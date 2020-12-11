from django.urls import path
from . import views
app_name="app_movies"
urlpatterns = [
    path("",views.MovieHome.as_view(),name="movies_home"),
    path("movies/<slug:slug>/",views.MovieDetail.as_view(),name="movies_detail"),
    path("movies/",views.MovieList.as_view(),name="movies_list"),
    path("search/",views.Search.as_view(),name="search"),
]
