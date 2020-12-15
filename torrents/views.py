from django.shortcuts import render
from .models import TorrentKeyword,Magnet
from django.contrib import messages
import datetime
from django.core.paginator import Paginator
from .torrentScrapper import TorrentInfo
from django.views.generic import View,DetailView
class TorrentHome(View):
    def query_and_save(self,query,torobj):
        torrents = TorrentInfo(query)
        torrents.num_pages(pages=1)
        results = torrents.json()
        for ndx in range(1,len(results)+1):
            ndx = results[str(ndx)]
            name,seeders,leechers,size,magnet,category = ndx.get("name","Unknown"),ndx.get("seeders",0),ndx.get("leechers",0),ndx.get("size","Unknown"),ndx.get("url","Unknown"),ndx.get("category","Unknown")
            magnet_object = Magnet.objects.filter(magnet=magnet)
            if not magnet_object.exists():
                magnet_object = Magnet.objects.create(
                    name=name,
                    seeders=seeders,
                    leechers=leechers,
                    size=size,
                    magnet=magnet,
                    category=category.upper()
                )
                magnet_object.torrent.add(torobj)
            else:
                magnet_object.first().torrent.add(torobj)
        # return torobj.torrent_magnet.all()
    def paginate(self,objects,num_of_obj,page):
        paginated = Paginator(objects,num_of_obj)
        results = paginated.page(page)
        return results
    def get(self,request,**kwargs):
        query = self.request.GET.get("query")
        if query:
            if len(query)>3 and len(query)<32:
                query = query.lower()
                torrent_object = TorrentKeyword.objects.filter(keyword=query)
 
                if not torrent_object.exists():
                    keyword = TorrentKeyword.objects.create(keyword=query)
                    # results = self.query_and_save(query,keyword)
                    self.query_and_save(query,keyword)
                else:
                    #if exits
                    now = datetime.date.today().day
                    then = torrent_object.first().added_on.day
                    escaped_day = now-then
                    # scrap every 5 days and if doesn't have magnet
                    if escaped_day > 5 or not torrent_object.first().torrent_magnet.all() :
                        # results = self.query_and_save(query,torrent_object)
                        self.query_and_save(query,torrent_object.first())
                    # else:
                        # results = torrent_object.first().torrent_magnet.all()
                results = Magnet.objects.filter(name__icontains=query)
                results = self.paginate(results,15,request.GET.get("page",1))
                return render(request,"torrents/torrent.html",{"objects":results})
            messages.info(request,"INVALID QUERY",fail_silently=True)
        return render(request,"torrents/torrent.html")
class TorrentDetail(DetailView):
    model = Magnet
    template_name="torrents/detail.html"
    context_object_name="torrent"