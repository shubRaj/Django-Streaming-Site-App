from django.urls import path
from . import views
app_name="app_movies"
urlpatterns = [
    path("",views.MovieHome.as_view(),name="movies_home"),
    path("<slug:slug>/",views.MovieDetail.as_view(),name="movies_detail"),
]
