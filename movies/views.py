from django.shortcuts import render
from .models import Movie,Cast,Term
from django.http import HttpResponseNotModified
from django.views.generic import (ListView,View,
DetailView,YearArchiveView
)
from .forms import CommentForm
from django.conf import settings
from django.contrib import messages
from django.core.mail.message import EmailMessage
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
    # def post(self,request,*args,**kwargs):
        
    #     return self.get(request,*args,**kwargs)
    def get(self,request,*args,**kwargs):
        # self.CommentForm = CommentForm()
        return super().get(request,*args,**kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.object.views +=1
        self.object.save(update_fields=["views",])
        context["related_movies"] = Movie.objects.filter(category__icontains=self.object.category).order_by("-uploaded_on")[:12]
        # context["CommentForm"]  = self.CommentForm
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
        objects = Movie.objects.filter(title__icontains=self.query)|Movie.objects.filter(category__icontains=self.query)\
            |Movie.objects.filter(language__icontains=self.query)|Movie.objects.filter(production__icontains=self.query).order_by("-uploaded_on")
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
        objects = Movie.objects.filter(status__icontains=self.status).order_by("-uploaded_on")
        return objects
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.queryset:
            #here i used set to prevent duplicacy
            context["recommended"] = {random.choice(Movie.objects.all()) for _ in range(20)}
        return context