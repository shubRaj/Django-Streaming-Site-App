from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets,generics
from movies.models import Movie
from datetime import date
from django.core.paginator import Paginator,EmptyPage
from .models import AdsConfig,AppConfig,PaymentConfig,ApkVersionInfo
from rest_framework.response import Response
from .serializers import (MovieSerializer,PaymentConfigSerializer,
AdsConfigSerializer,ApkVersionInfoSerializer,AppConfigSerializer)
from rest_framework.decorators import api_view,permission_classes
from itertools import chain
from rest_framework.permissions import IsAuthenticated
import requests,json
from movies.models import CATEGORY_CHOICES,LANGUAGE_CHOICES
from rest_framework.pagination import PageNumberPagination
year = date.today().year
class ResultsPagination(PageNumberPagination):
    page_size = 27
    page_size_query_param = 'page_size'
class MovieListAPI(viewsets.ModelViewSet):
    queryset= Movie.objects.all()
    pagination_class = ResultsPagination
    serializer_class = MovieSerializer
    def list(self,request,*args,**kwargs):
        results = super(MovieListAPI,self).list(request,*args,**kwargs).data.get("results")
        results = [{"videos_id":str(result.get("id")),
            "title":result.get("title"),
            "description":result.get("description"),
            "slug":result.get("slug"),
            "release":result.get("production"),
            "is_paid":"0",
            "is_tvseries":"0",
            "video_quality":"Auto",
            "thumbnail_url":result.get("poster"),
            "poster_url":result.get("banner")} for result in results]
        return Response(results)
class HomeAPI(viewsets.ViewSet):
    permission_classes = ()
    def list(self,request,*args,**kwargs):
        featured = Movie.objects.filter(status__contains="featured")[:10]
        latest_movies = [movie for movie in Movie.objects.all()[:18] if movie not in featured]
        results = {
            "slider":{
                "slider_type":"movie",
                "slide":[ 
                        {"id":str(movie.id),
                        "title":movie.title,
                        "description":movie.description,
                        "image_link":f"http://{request.get_host()}{movie.banner.url}",
                        "slug":movie.slug,
                        "action_type":movie.__class__.__name__.lower(),
                        "action_id":str(movie.id),
                        "action_btn_text":"Play",
                        "action_url":"",
                        } for movie in featured
                    ],
            },
            "all_country":[],
            "all_genre":[{"genre_id":category[0],"name":category[1],"description":"","slug":category[0],"url":"",
            "image_url":"genre.png"#place image
            } for category in CATEGORY_CHOICES],
            "featured_tv_channel":[],
            "latest_movies":[
                {
                    "videos_id":str(movie.id),
                    "title":movie.title,
                    "description":movie.description,
                    "slug":movie.slug,
                    "release":movie.production.year,
                    "is_paid":"0",
                    "runtime":"{} Mins".format(movie.runtime),
                    "video_quality":"Auto",
                    "thumbnail_url":f"http://{request.get_host()}{movie.poster.url}",
                    "poster_url":f"http://{request.get_host()}{movie.banner.url}"
                } for movie in latest_movies
            ],
            "latest_tvseries":[],
            "features_genre_and_movie":[],
            


        }
        return Response(results)
class AllGenreAPI(viewsets.ViewSet):
    permission_classes = ()
    pagination_class = ResultsPagination
    def list(self,request,*args,**kwargs):
        genres = [
            {
                "genre_id":genre[0],
                "name":genre[1],
                "description":genre[1],
                "slug":genre[0],
                "url":"",
                "image_url":"genre.png",#place image
            } for genre in CATEGORY_CHOICES
            ]
        
        return Response(genres)
class ContentByGenre(viewsets.ViewSet):
    permission_classes = ()
    def list(self,request,*args,**kwargs):
        genre_id = request.GET.get("id")
        page = request.GET.get("page","1")
        if genre_id and page:
            movies = Movie.objects.filter(category__contains=genre_id)[:40]
            try:
                paginated = Paginator(movies,9)
                movies  = paginated.page(page)
            except EmptyPage:
                return Response({})
            results = [
                {
                    "videos_id":str(movie.id),
                    "title":movie.title,
                    "description":movie.description,
                    "slug":movie.slug,
                    "release":movie.production.year,
                    "is_paid":"0",
                    "is_tvseries":"0",
                    "video_quality":"Auto",
                    "thumbnail_url":f"http://{request.get_host()}{movie.poster.url}",
                    "poster_url":f"http://{request.get_host()}{movie.banner.url}"
                } for movie in movies
            ]
            return Response(results)
        return Response({})
# class LoginAPI(viewsets.ViewSet):
#     permission_classes = ()
#     def list(self,request,*args,**kwargs):
#         print(request.POST)
#         return Response({})
class AllCountryAPI(viewsets.ViewSet):
    permission_classes = ()
    def list(self,request,*args,**kwargs):
        genres = [
            {
                "genre_id":language[0],
                "name":language[1],
                "description":language[1],
                "slug":language[0],
                "url":"",
                "image_url":"country.png",#place image
            } for language in LANGUAGE_CHOICES
        ]
        
        return Response(genres)
class SearchAPI(viewsets.ViewSet):
    permission_classes = ()
    def list(self,request,*args,**kwargs):
        query = request.GET.get("q")
        video_type = request.GET.get("type","movietvserieslive")
        range_to = date(int(request.GET.get("range_to",year)),12,31)
        range_from = date(int(request.GET.get("range_from",1990)),1,1)
        tv_category_id = int(request.GET.get("tv_category_id","0"))
        genre_id = int(request.GET.get("genre_id","0"))
        country_id = int(request.GET.get("country_id","0"))
        if genre_id ==0:
            genre_id = ""
        else:
            genre_id = CATEGORY_CHOICES[genre_id-1][0]
        if country_id ==0:
            country_id = ""
        else:
            country_id = LANGUAGE_CHOICES[country_id-1][0]
        # if tv_category_id !=0:
        #     tv_category_id -=1
        results = {
            "movie":[],
            "tvseries":[],
            "tv_channels":[]
        }
        if "movie" in video_type:
            results["movie"].extend([
                {
                    "videos_id":movie.id,
                    "title":movie.title,
                    "description":movie.description,
                    "slug":movie.slug,
                    "release":movie.production.year,
                    "runtime":"{} Mins".format(movie.runtime),
                    "is_tvseries":"0",
                    "video_quality":"Auto",
                    "thumbnail_url":f"http://{request.get_host()}{movie.banner.url}",
                    "poster_url":f"http://{request.get_host()}{movie.poster.url}",
                } for movie in Movie.objects.filter(language__contains=country_id).filter(category__contains=genre_id).filter(production__range=(range_from,range_to)).filter(title__icontains=query)[:40]
            ])
        return Response(results)
class SingleDetailAPI(viewsets.ViewSet):
    permission_classes = ()
    def list(self,request,*args,**kwargs):
        video_id=request.GET.get("id",None)
        video_type = request.GET.get("type",None)
        if video_type =="movie" and video_id:
            queryset = Movie.objects.get(id=video_id)
            serializer_data = MovieSerializer(queryset).data
            movie = {
                "videos_id":video_id,
                "title":serializer_data.get("title"),
                "description":serializer_data.get("description"),
                "slug":serializer_data.get("slug"),
                "rating":serializer_data.get("rating"),
                "audio":serializer_data.get("language"),
                "release":serializer_data.get("production"),
                "runtime":"{} Mins".format(serializer_data.get("runtime")),
                "video_quality":"Auto",
                "is_tvseries":"0",
                "is_paid":"0",
                "enable_download":"0",
                "download_links":[
                    {
                        "video_file_id":str(torrent.id),
                        "label":".torrent File",
                        "videos_id":str(queryset.id),
                        "resolution":torrent.quality,
                        "file_size":"",
                        "download_url":torrent.link,
                        "in_app_download":False,
                    } for torrent in queryset.movie_torrent.all()
                ]+[
                    {
                        'download_link_id':str(download.id),
                        "label":download.quality,
                        "videos_id":queryset.id,
                        "resolution":download.quality,
                        "file_size":"",
                        "download_url":download.link,
                        "in_app_download":True,

                    } for download in queryset.movie_download.all()
                ],
                "thumbnail_url":f"http://{request.get_host()}{serializer_data.get('poster')}",
                "poster_url":f"http://{request.get_host()}{serializer_data.get('banner')}",
                "videos":[
                        {"video_file_id":str(video.id),
                        "label":video.quality,
                        "streak_key":"",
                        "file_type":"embed",
                        "file_url":video.link,
                        "subtitle":[],
                        } for video in queryset.movie_embed.all()
                    ]+[
                      {"video_file_id":"0",
                            "label":magnet.quality+" - Torrent Player",
                            "streak_key":"",
                            "file_type":"embed",
                            "file_url":f"http://{request.get_host()}/apps/embed/?magnet={magnet.link}",
                            "subtitle":[],
                        } for magnet in queryset.movie_magnet.all() if magnet.quality
                    ]+[
                      {"video_file_id":"0",
                            "label":download.quality,
                            "streak_key":"",
                            "file_type":"mp4",
                            "file_url":download.link,
                            "subtitle":[],
                        } for download in queryset.movie_download.all()
                    ],
                "genre":[{"genre":genre,"name":genre,"url":""} for genre in serializer_data.get("category")],
                "country":[],
                "director":[],
                "writer":[],
                "cast":[
                    {"star_id":str(cast.id),
                    "name":cast.name,
                    "url":"",
                    "image_url":f"http://{request.get_host()}{cast.image.url}"} for cast in queryset.movie_cast.all()
                ],
                "cast_and_crew":[],
                "related_movie":[
                    {
                    "videos_id":_movie.id,
                    "genre":"",
                    "country":"",
                    "title":_movie.title,
                    "description":_movie.description,
                    "slug":_movie.slug,
                    "is_paid":"0",
                    "is_tvseries":"0",
                    "release":_movie.production,
                    "runtime":"{} Mins".format(_movie.runtime),
                    "video_quality":"Auto",
                    "thumbnail_url":f"http://{request.get_host()}{_movie.poster.url}",
                    "poster_url":f"http://{request.get_host()}{_movie.banner.url}",
                    } for _movie in Movie.objects.all()[:18]
                ],
            }
            movie["videos"].append({"video_file_id":"0",
                            "label":"Trailer",
                            "streak_key":"",
                            "file_type":"embed",
                            "file_url":serializer_data.get("trailer","https://youtube.com/embed/"),
                            "subtitle":[],
                        })
            if queryset.movie_download.exists() or queryset.movie_torrent.exists():
                movie["enable_download"] = "1"
            return Response(movie)
        return Response({})
@api_view(["GET",])
@permission_classes([IsAuthenticated,])
def basic_config(request):
    if request.method =="GET":
        adsconfig = AdsConfigSerializer(AdsConfig.objects.all(),many=True)
        paymentconfig = PaymentConfigSerializer(PaymentConfig.objects.all(),many=True)
        appconfig = AppConfigSerializer(AppConfig.objects.all(),many=True)
        apkversioninfo = ApkVersionInfoSerializer(ApkVersionInfo.objects.all(),many=True)
        #genre_id starts with 1. 0 means all.this is done for basic_config only because search 
        #crashes when category[0] is used.
        genres  = [{"genre_id":str(CATEGORY_CHOICES.index(category)+1),"name":category[1],"description":"","slug":category[0],"url":""
            ,"image_url":"genre.png"#place image
            } for category in CATEGORY_CHOICES]
        #same here
        countries = [
            {
                'country_id':str(LANGUAGE_CHOICES.index(country)+1),
                "name":country[1],
                "description":country[1],
                "slug":country[1],
                "url":"",
                "image_url":"country.png"
            } for country in LANGUAGE_CHOICES
        ]
        basic_config = {
           "app_config":appconfig.data[0],
           "ads_config":adsconfig.data[0],
           "payment_config":paymentconfig.data[0],
           "apk_version_info":apkversioninfo.data[0],
           "genre":genres,
           "country":countries,
           "tv_category":[],
        }
        return Response(basic_config)