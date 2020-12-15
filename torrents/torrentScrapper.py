#! /usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import urllib
import json
class TorrentInfo:
    def __init__(self,search):
        self.currentNdx=1
        self.search=urllib.parse.quote(search,safe="")
        self.items={}
        self.item_id=0
        try:
            self.totalNdx=int(self.soup().find("div",{"class":"pagination"}).find_all("li")[-1].text.strip())
        except:
            self.totalNdx=self.currentNdx
    def soup(self):
        re = requests.get(f"https://www.1377x.to/search/{self.search}/{self.currentNdx}/")
        soup = BeautifulSoup(re.content,"html.parser")
        return soup
    def __str__(self):
        return self.search
    def num_pages(self,pages=None):
        if pages and isinstance(pages,int):
            self.totalNdx=pages
        return self.totalNdx
    def urls(self):
        while self.currentNdx <= self.totalNdx:
            #print(f"Scrapping Page: {self.currentNdx}")
            for items in self.soup().find_all("tr")[1:]:
                self.item_id+=1
                self.items[str(self.item_id)]={"name":items.find("td",{"class":"coll-1 name"}).text.strip(),
                "seeders":items.find("td",{"class":"coll-2 seeds"}).text.strip(),
                "leechers":items.find("td",{"class":"coll-3 leeches"}).text.strip(),
                "size":items.find("td",{"class":"coll-4 size mob-uploader"}).text.strip(),
                "url":items.find("td",{"class":"coll-1 name"}).find_all("a")[1]["href"],     
                }
            self.currentNdx +=1
        return self.items
    def json(self):
        for item in self.urls():
            re = requests.get(f"https://www.1377x.to{self.items[item]['url']}")
            soup = BeautifulSoup(re.content,'html.parser')
            for detail in soup.find_all("li"):
                
                if detail.text.strip()=="Magnet Download":
                    self.items[item].update(url=detail.find("a")["href"])
                elif "Category" in detail.text:
                    self.items[item].update(category=detail.text.lstrip("Category"))
        return self.items
if __name__=="__main__":
    c1 = TorrentInfo("django movie")
    print(c1.json())
