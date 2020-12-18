from django.shortcuts import render
from .models import Movie,Cast,Term,Torrent,Magnet,Embed
from django.urls import reverse
from django.core.paginator import  Paginator
from django.http import HttpResponseNotModified,HttpResponseRedirect
from django.views.generic import (ListView,View,
DetailView,YearArchiveView
)
from torrents.torrentScrapper import TorrentInfo
from itertools import chain
from .tmdbAPI import TMDBAPI
from .forms import CommentForm
from django.conf import settings
from django.contrib.auth.models import User,Group
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib import messages
from django.core.mail.message import EmailMessage
from .ytsmx import YTSMX
import random
from .desicinemaAPI import DesiCinemaAPI
from django.utils.text import slugify
class MovieHome(ListView):
    model = Movie
    template_name="movies/home.html"
    context_object_name="movies"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recent"] = Movie.objects.all()[0:8]
        context["featured"] = Movie.objects.filter(status__icontains="featured")[:8]
        context["mostwatched"] = Movie.objects.filter(status__icontains="mostwatched")[:8]
        return context
class MovieDetail(DetailView):
    model = Movie
    template_name = 'movies/detail.html'
    context_object_name = "movie"
    # def post(self,request,*args,**kwargs):
        
    #     return self.get(request,*args,**kwargs)
    def get(self,request,*args,**kwargs):
        # self.CommentForm = CommentForm()
        return super().get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views +=1
        self.object.save(update_fields=["views",])
        context["related_movies"] = Movie.objects.filter(category__icontains=self.object.category).all()[:12]
        # context["CommentForm"]  = self.CommentForm
        return context
class MovieList(ListView):
    model = Movie
    paginate_by = 40
    template_name="movies/list.html"
    context_object_name = "movies"
    def get_queryset(self):
        self.queryset = Movie.objects.all()[:120]
        return super().get_queryset()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.queryset:
            #here i used set to prevent duplicacy
            movies = Movie.objects.all()
            context["recommended"] = {random.choice(movies) for _ in range(20)}
        return context
    
class Search(MovieList):
    def get(self,request,*args,**kwargs):
        self.query = self.request.GET.get("query")
        if not self.query:
            return HttpResponseNotModified()
        return super().get(request,*args,**kwargs)
    def get_queryset(self):
        objects = Movie.objects.filter(title__icontains=self.query)|Movie.objects.filter(category__icontains=self.query)\
            |Movie.objects.filter(language__icontains=self.query)|Movie.objects.filter(production__icontains=self.query).all()
        casts = Cast.objects.filter(name__icontains=self.query)
        #movies of each cast
        for cast in casts:
            cast_movies = [movie for movie in cast.movie.all() if movie not in objects]
            objects = list(chain(objects,cast_movies))
        return objects
class MovieByYear(YearArchiveView):
    paginate_by = 40
    date_field = "production"
    make_object_list = True
    allow_future = True
    context_object_name="movies"
    template_name = "movies/list.html"
    queryset = Movie.objects.all()

def terms_and_condition(request):
    terms = Term.objects.all()
    return render(request,"movies/terms.html",{"terms":terms})
class Contact(View):
    def get(self,request,*args,**kwargs):
        return render(request,"contact.html")
    def post(self,request,*args,**kwargs):
        name = self.request.POST.get("name")
        email = self.request.POST.get("email")
        service = self.request.POST.get("service")
        message = self.request.POST.get("message")
        try:
            email = EmailMessage(subject=f"{service}[{email}]",to=["shuvraj1234@gmail.com",],from_email=settings.EMAIL_HOST_USER)
            email.send()
            messages.add_message(request,messages.SUCCESS,f"Thank You {name} For Query,We'll Get Back To You ASAP",fail_silently=True)
        except:
            messages.add_message(request,messages.ERROR,f"Sorry {name},Your Query Wasn't Unable To Send Successfully",fail_silently=True)
        return render(request,"contact.html")
class MovieStatus(ListView):
    model = Movie
    template_name="movies/list.html"
    context_object_name="movies"
    paginate_by=40
    def get(self,request,*args,**kwargs):
        self.status = self.kwargs.get("status")
        if not self.status:
            return HttpResponseNotModified()
        return super().get(request,*args,**kwargs)
    def get_queryset(self):
        objects = Movie.objects.filter(status__icontains=self.status).all()
        return objects
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.queryset:
            #here i used set to prevent duplicacy
            context["recommended"] = {random.choice(Movie.objects.all()) for _ in range(20)}
        return context
class AddContent(UserPassesTestMixin,View):
    def get(self,request,tmdbId):
        tmdb = TMDBAPI()
        if tmdbId:
            try:
                poster_base_url = getattr(tmdb,"poster_base_url")
                banner_base_url = getattr(tmdb,"banner_base_url")
                movie_info = tmdb.get(tmdbId)
                if not Movie.objects.filter(imdbID=movie_info.get("imdb_id")).exists():
                    casts = tmdb.get_casts(tmdbId)
                    genres = [genre.get("name").lower() for genre in movie_info.get("genres")]
                    languages = [language.get("iso_639_1") for language in movie_info.get("spoken_languages")]
                    backdrop = movie_info.get("backdrop_path")
                    if not backdrop:
                        backdrop = None
                    else:
                        backdrop = banner_base_url+backdrop
                    movie = Movie(
                        title=movie_info.get("title"),
                        imdbID=movie_info.get("imdb_id"),
                        posterURL=f'{poster_base_url}{movie_info.get("poster_path")}',
                        bannerURL = backdrop,
                        category = genres,
                        language = languages,
                        tagline = movie_info.get("tagline"),
                        description = movie_info.get("overview"),
                        trailer = f"https://www.youtube.com/embed/{movie_info.get('trailer')}",
                        rating = movie_info.get("vote_average",0.0),
                        runtime = movie_info.get("runtime"),
                        production = movie_info.get("release_date")
                    )
                    movie.save(commit=False)
                    if casts:
                        for cast in casts:
                            if Cast.objects.filter(name=cast.name).exists():
                                Cast.objects.get(name=cast.name).movie.add(movie)
                            else: 
                                if not cast.image:
                                    Cast.objects.create(name=cast.name,).movie.add(movie)
                                else:
                                    Cast.objects.create(name=cast.name,imageURL=f"{poster_base_url}{cast.image}").movie.add(movie)
                    ytsmx = YTSMX(f"https://yts.mx/movies/{movie.slug}")
                    torrents = ytsmx.get_torrent()
                    magnets = ytsmx.get_magnet()
                    if not(torrents or magnets):
                        scrap_1377x = TorrentInfo(movie.title.lower())
                        scrap_1377x.num_pages(1)
                        results = scrap_1377x.json()
                        if results:
                            magnets = [results[result].get("url") for result in results]
                            for magnet in magnets[0:4]:
                                Magnet.objects.create(movie=movie,link=magnet)
                    else:
                        if torrents:
                            for torrent in torrents:
                                Torrent.objects.create(movie=movie,quality=torrent.quality,link=torrent.download)
                        if magnets:
                            for magnet in magnets:
                                Magnet.objects.create(movie=movie,quality=magnet.quality,link=magnet.magnet)
                    #for bollywood movie scrap from desicinema.tv
                    #if hindi language in movie.language
                    if "hi" in movie.language:
                        embedlinks = DesiCinemaAPI(f"https://desicinemas.tv/movies/{slugify(movie.title)}").get_embedlinks()
                        if embedlinks:
                            for embedlink in embedlinks:
                                Embed.objects.create(quality="HD",link=embedlink,movie=movie)
                    movie.save()
                    messages.success(request,f"{movie_info.get('title')} Added Successfully",fail_silently=True)
                else:
                    messages.info(request,f"{movie_info.get('title')} Exists",fail_silently=True)
            except Exception:
                messages.error(request,"Couldn't Added The Content",fail_silently=True)
        else:
            query = request.GET.get("query")
            if query:
                page = request.GET.get("page",1)
                objects = [item for item in tmdb.search(query) if item.get("poster_path")]
                paginated = Paginator(objects,15)
                objects_on_page = paginated.page(page)
                context = {
                    "objects":objects_on_page,
                }
                if not objects_on_page:
                    messages.info(request,"No Result Found",fail_silently=True)
                return render(request,"add_content.html",context)
        return render(request,"add_content.html")
    def test_func(self):
        return self.request.user.groups.filter(name="Manager").exists() or self.request.user.is_superuser
    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("app_movies:movies_home"))