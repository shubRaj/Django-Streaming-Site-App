from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User
from PIL import Image
import string,random
import datetime
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
LANGUAGE_CHOICES = settings.LANGUAGES
STATUS_CHOICES = (
    ("featured","FEATURED"),
    ("mostwatched","MOST WATCHED"),
)
TAG_CHOICES=(
    ("footer","FOOTER"),
    ("header","HEADER"),
    ("body","BODY"),
)
def resize_image(original_image,image_name,image_size):
    image = Image.open(original_image)
    if image.width!=image_size[0] or image.height!=image_size[1]:
        image.thumbnail(image_size)
        if "poster" in image_name:
            image.save(Path(settings.MEDIA_ROOT)/f"poster/{image_name}")
        elif "cast" in image_name:
            image.save(Path(settings.MEDIA_ROOT)/f"casts/{image_name}")
        else:
            image.save(Path(settings.MEDIA_ROOT)/f"banner/{image_name}")
    else:
        if "poster" in image_name:
            image.save(Path(settings.MEDIA_ROOT)/f"poster/{image_name}")
        elif "cast" in image_name:
            image.save(Path(settings.MEDIA_ROOT)/f"casts/{image_name}")
        else:
            image.save(Path(settings.MEDIA_ROOT)/f"banner/{image_name}")
    os.remove(original_image)
def downloadImage(image_url,image_name,image_size):
    r = requests.get(image_url)
    size = round(int(r.headers.get("content-length"))/(1024*1024))
    if size <=10:
        imageBytes = r.content
        content_disposition = r.headers.get("content-disposition")
        if content_disposition:
            original_image = content_disposition.split('"')[-2]
            image_extension = original_image.split(".")[-1]
        else:
            chars = string.ascii_letters
            original_image = "".join([random.choice(chars) for _ in range(2)])
            image_extension = "jpg"
            original_image+="."+image_extension
        image_name = f'{image_name}.{image_extension}'
        original_image = Path(settings.MEDIA_ROOT)/original_image
        with open(original_image,"wb") as f:
            f.write(imageBytes)
        resize_image(original_image,image_name,image_size)
    return image_name
class Movie(models.Model):
    title = models.CharField(max_length=200)
    imdbID = models.CharField(max_length=16,null=True,blank=True,unique=True)
    posterURL = models.URLField(max_length=2083,null=True,blank=True)
    bannerURL = models.URLField(max_length=2083,null=True,blank=True)
    poster = models.ImageField(upload_to="poster",default="poster/poster.jpg")
    banner = models.ImageField(upload_to="banner",default="banner/banner.jpg")
    category = MultiSelectField(choices=CATEGORY_CHOICES,max_length=100,max_choices=4,null=True)
    language = MultiSelectField(choices=LANGUAGE_CHOICES,max_length=100,max_choices=3,null=True)
    status = MultiSelectField(choices=STATUS_CHOICES,max_length=30,max_choices=3,null=True,blank=True)
    tagline = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(blank=True,null=True)
    trailer = models.URLField(blank=True,null=True)
    rating = models.DecimalField(decimal_places=1,blank=True,max_digits=2,null=True)
    runtime = models.IntegerField(null=True,blank=True,validators=[MaxValueValidator(200)])
    download= models.URLField(blank=True,null=True)
    views = models.IntegerField(default=0)
    slug = models.SlugField(blank=True,max_length=283)
    production = models.DateField(null=True,blank=True,default=datetime.date.today)
    uploaded_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return f"{self.title}"
    def save(self,*args,**kwargs):
        if not self.slug:
            # date_time_obj = datetime.datetime.strptime(self.production,"%Y-%m-%d")
            year = self.production.split("-")[0]
            self.slug = f"{slugify(self.title)}-{year}"
        with ThreadPoolExecutor(max_workers=2) as executor:
            #and self._meta.get_field("poster").default in self.poster.path
            if self.posterURL:
                posterThread = executor.submit(downloadImage,self.posterURL,f"{self.imdbID}-poster",(200,300))
                self.poster = f"poster/{posterThread.result()}"
                self.posterURL = None
            if self.bannerURL:
                bannerThread = executor.submit(downloadImage,self.bannerURL,f"{self.imdbID}-banner",(1920,1080))
                self.banner = f"banner/{bannerThread.result()}"
                self.bannerURL = None
        super(Movie,self).save(*args,**kwargs)
class Cast(models.Model):
    movie = models.ManyToManyField(Movie,related_name="movie_cast")
    name = models.CharField(max_length=50,null=True,unique=True)
    imageURL = models.URLField(blank=True,null=True)
    image = models.ImageField(upload_to="casts",default="casts/casts.jpg")
    def save(self,*args,**kwargs):
        with ThreadPoolExecutor(max_workers=1) as executor:
            if self.imageURL:
                imageThread = executor.submit(downloadImage,self.imageURL,f"{self.name}-cast",(180,180))
                self.image = f"casts/{imageThread.result()}"
                self.imageURL = None
        super(Cast,self).save(*args,**kwargs)
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
    commented_on = models.DateTimeField(default=timezone.now,editable=False)
    def __str__(self):
        return self.comment
    class Meta:
        ordering=["-commented_on"]
class AbsTag(models.Model):
    portion = MultiSelectField(choices=TAG_CHOICES,max_choices=3,max_length=30)
    tag = models.CharField(max_length=50)
    class Meta:
        abstract=True
class StaticTag(AbsTag):
    class Meta:
        verbose_name="StaticTag"
class DynamicTag(AbsTag):
    movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="movie_tag")
    class Meta:
        verbose_name="DynamcTag"
class Term(models.Model):
    paragraph = models.TextField()
    created_on = models.DateTimeField(default=timezone.now,editable=False)