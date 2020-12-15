from django.urls import re_path,path
from . import views
app_name="app_movies"
urlpatterns = [
    path("terms-and-conditions/",views.terms_and_condition,name="terms"),
    path("contact/",views.Contact.as_view(),name="contact"),
    path("movie/<slug:slug>/",views.MovieDetail.as_view(),name="movies_detail"),
    path("movies/",views.MovieList.as_view(),name="movies_list"),
    path("search/",views.Search.as_view(),name="search"),
    path("year/<int:year>/",views.MovieByYear.as_view(),name="movies_year"),
    re_path(r"^add/(?P<tmdbId>\w*)/?$",views.AddContent.as_view(),name="add_content"),
    path("status/<str:status>/",views.MovieStatus.as_view(),name="movies_status"),
    path("",views.MovieHome.as_view(),name="movies_home"),
]
