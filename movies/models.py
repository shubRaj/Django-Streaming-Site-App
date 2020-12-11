from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from PIL import Image
import requests
from concurrent.futures import ThreadPoolExecutor
from django.conf import settings
from pathlib import Path
import os
CATEGORY_CHOICES = (
    ("action","ACTION"),
    ("drama","DRAMA"),
    ("comedy","COMEDY"),
    ("romance","ROMANCE"),# category of the movie ***Note:-don't make first keyword like action -->Action becoz we need to access it by same form i.e /Action
    ("adventure","ADVENTURE"),
    ("animation","ANIMATION"),
    ("crime","CRIME"),
    ("documentary","DOCUMENTARY"),
    ("family","FAMILY"),
    ("fantasy","FANTASY"),
    ("horror","HORROR"),
    ("music","MUSIC"),
    ("scifi","SCI-FI"),
    ("thriller","THRILLER"),
    ("war","WAR"),   
)
LANGUAGE_CHOICES = (
    ("en","ENGLISH"),
    ("hi","HINDI"),
    ("ch","CHINESE"),
    ("pun","PUNJABI")
)
STATUS_CHOICES = (
    ("featured","FEATURED"),
    ("mostwatched","MOST WATCHED"),
)
def resize_image(original_image,image_name,image_size):
    image = Image.open(original_image)
    if image.width>image_size[0] or image.height>image_size[1]:
        image.thumbnail(image_size)
        if "poster" in image_name:
            image.save(Path(settings.MEDIA_ROOT)/f"poster/{image_name}")
        else:
            image.save(Path(settings.MEDIA_ROOT)/f"banner/{image_name}")
        os.remove(original_image)
def downloadImage(image_url,image_name,image_size):
    r = requests.get(image_url)
    size = round(int(r.headers.get("content-length"))/(1024*1024))
    if size <=10:
        imageBytes = r.content
        original_image = r.headers.get("content-disposition").split('"')[-2]
        image_extension = original_image.split(".")[-1]
        image_name = f'{image_name}.{image_extension}'
        original_image = Path(settings.MEDIA_ROOT)/original_image
        with open(original_image,"wb") as f:
            f.write(imageBytes)
        resize_image(original_image,image_name,image_size)
    return image_name
class Movie(models.Model):
    title = models.CharField(max_length=200)
    imdbID = models.IntegerField(null=True,blank=True,unique=True)
    posterURL = models.URLField(max_length=2083,null=True,blank=True)
    bannerURL = models.URLField(max_length=2083,null=True,blank=True)
    poster = models.ImageField(upload_to="poster",default="poster/poster.jpg")
    banner = models.ImageField(upload_to="banner",default="banner/banner.jpg")
    category = MultiSelectField(choices=CATEGORY_CHOICES,max_length=40,max_choices=4,null=True)
    language = MultiSelectField(choices=LANGUAGE_CHOICES,max_length=30,max_choices=3,null=True)
    status = MultiSelectField(choices=STATUS_CHOICES,max_length=30,max_choices=3,null=True,blank=True)
    tagline = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    trailer = models.URLField(blank=True,null=True)
    rating = models.DecimalField(decimal_places=1,blank=True,max_digits=2,null=True)
    runtime = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(200)])
    download= models.URLField(blank=True,null=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,max_length=283)
    production = models.DateField(null=True,blank=True)
    uploaded_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return f"{self.title}"
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = f"{slugify(self.title)}-{self.imdbID}"
        with ThreadPoolExecutor(max_workers=2) as executor:
            if self.posterURL and self._meta.get_field("poster").default in self.poster.path:
                posterThread = executor.submit(downloadImage,self.posterURL,f"{self.imdbID}-poster",(200,300))
                self.poster = f"poster/{posterThread.result()}"
            if self.bannerURL and self._meta.get_field("banner").default in self.banner.path:
                bannerThread = executor.submit(downloadImage,self.bannerURL,f"{self.imdbID}-banner",(1280,720))
                self.banner = f"banner/{bannerThread.result()}"
        super(Movie,self).save(*args,**kwargs)
class Cast(models.Model):
    movie = models.ManyToManyField(Movie,related_name="movie_cast")
    name = models.CharField(max_length=50,null=True,unique=True)
    image = models.ImageField(upload_to="casts",default="casts/casts.jpg")
    actress = models.BooleanField(default=True)
class TorAbs(models.Model):
    quality = models.CharField(max_length=30,null=True,blank=True)
    link = models.URLField(max_length=2083)
    class Meta:
        abstract=True
class Torrent(TorAbs):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_torrent")
class Magnet(TorAbs):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_magnet")
    link = models.CharField(max_length=2083)
class WebTor(models.Model):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_webtor")
    quality = TorAbs._meta.get_field("quality")
    source = models.CharField(max_length=2083)
    class Meta:
        verbose_name="Webtor"
class Embed(TorAbs):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_embed")
class Download(TorAbs):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_download")
class Comment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_comment",null=True,blank=True)
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_comment",null=True)
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.comment
    class Meta:
        ordering=["-created_on"]
