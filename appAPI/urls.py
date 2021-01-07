from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (MovieListAPI,SingleDetailAPI,
AllCountryAPI,HomeAPI,AllGenreAPI,SearchAPI,ContentByGenre)
from django.views.generic import TemplateView
router = DefaultRouter()
router.register("movies",MovieListAPI,basename="moviesapi")
router.register("home_content_for_android",HomeAPI,basename="homeapi")
router.register("all_genre",AllGenreAPI,basename="allgenreapi")
router.register("all_country",AllCountryAPI,basename="allcountryapi")
router.register("search",SearchAPI,basename="searchapi")
router.register("content_by_genre_id",ContentByGenre,basename="contentbygenreapi")
router.register("single_details",SingleDetailAPI,basename="singledetailsapi")
from . import views
app_name = "apprestapi"
urlpatterns=[
    path("",include((router.urls,"restapp"),namespace="rest_home")),
    path("config/",views.basic_config,name="basic_config"),
    path("embed/",TemplateView.as_view(template_name="appAPI/embed.html"),name="embed"),

]