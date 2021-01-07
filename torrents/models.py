from django.db import models
import uuid
class TorrentKeyword(models.Model):
    keyword = models.CharField(max_length=250,unique=True)
    added_on = models.DateField(auto_now_add=True,editable=False)
    class Meta:
        ordering=["-added_on"]
    def __str__(self):
        return self.keyword
class Magnet(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    torrent = models.ManyToManyField(TorrentKeyword,related_name="torrent_magnet")
    name=models.CharField(max_length=2083)
    category = models.CharField(max_length=30)
    seeders = models.IntegerField(default=0)
    leechers = models.IntegerField(default=0)
    size = models.CharField(max_length=10,blank=True,null=True)
    magnet = models.TextField(null=True,unique=True)
    added_on = models.DateTimeField(auto_now=True,editable=False)
    def __str__(self):
        return f"{self.name}"
    class Meta:
        ordering = ["-seeders","-leechers"]