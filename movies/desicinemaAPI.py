from bs4 import BeautifulSoup
import requests
class DesiCinemaAPI:
    def __init__(self,url):
        r = requests.get(url).content
        soup = BeautifulSoup(r,"html.parser")
        watchlinks = [watchlink["href"] for watchlink in soup.find_all("a",{"class":"Button"}) if watchlink.text=="Click Here"]
        self.embedlinks = [BeautifulSoup(requests.get(embedlink).content,"html.parser").find("iframe").get("src") for embedlink in watchlinks]
    def get_embedlinks(self):
        return self.embedlinks
if __name__=="__main__":
    movie = DesiCinemaAPI("https://desicinemas.tv/movies/sdsd")
    print(movie.get_embedlinks())