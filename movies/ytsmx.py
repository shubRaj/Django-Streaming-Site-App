import requests
from bs4 import BeautifulSoup
from collections import namedtuple
class YTSMX:
    def __init__(self,url):
        r = requests.get(url).content
        soup = BeautifulSoup(r,"html.parser")
        self.torrent_p = soup.find("p",{"class":"hidden-sm",})
        self.magnet_div = soup.find_all("div",{"class":"modal-torrent",})
        self.torrent = namedtuple("torrent",("quality","download"))
        self.magnet = namedtuple("magnet",("quality","magnet"))
        self.torrentDownload = []
        self.magnetDownload = []
    def get_torrent(self):
        if self.torrent_p:
            for torrentlink in self.torrent_p.find_all("a"):
                if "https://yts.mx/" in torrentlink["href"]:
                    self.torrentDownload.append(self.torrent(torrentlink.text,torrentlink["href"]))
            return self.torrentDownload
        return []
    def get_magnet(self):
        if self.magnet_div:
            for magnetlinks in self.magnet_div:
                for magnetlink in magnetlinks.find_all("a",{"class":"magnet-download"}):
                    self.magnetDownload.append(self.magnet(magnetlink["title"].split()[-2],magnetlink["href"]))
            return self.magnetDownload
        return []