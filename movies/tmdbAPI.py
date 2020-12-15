import requests
from configparser import ConfigParser
config = ConfigParser()
config.read("config.cfg")
API_KEY = config["TMDBAPI"]["api_key"]
from collections import namedtuple
class TMDBAPI:
    """
    Happy Coding
    """
    poster_base_url = "https://image.tmdb.org/t/p/w500"
    banner_base_url = "https://image.tmdb.org/t/p/original"
    imdb_content = "https://api.themoviedb.org/3/find/%s?api_key=%s&language=en-US&external_source=imdb_id"
    get_imdb_id = "https://api.themoviedb.org/3/%s/%s/external_ids?api_key=%s"
    single_detail = "https://api.themoviedb.org/3/%s/%s?api_key=%s"
    query_base_url = "https://api.themoviedb.org/3/search/%s?api_key=%s&query=%s"
    video_base_url = 'https://api.themoviedb.org/3/%s/%s/videos?api_key=%s'
    # language_base_url = "https://api.themoviedb.org/3/configuration/languages?api_key=%s"
    # genre_base_url = "https://api.themoviedb.org/3/genre/movie/list?api_key=%s"
    cast_base_url = "https://api.themoviedb.org/3/%s/%s/credits?api_key=%s"
    def __init__(self, *args, **kwargs):
        pass
        # self._genres = requests.get(self.genre_base_url % API_KEY).json()
        # self._languages = requests.get(self.language_base_url % API_KEY).json()
    def from_imdbId(self,imdbId):
        results = requests.get(self.imdb_content % (imdbId, API_KEY)).json().get("movie_results")
        if not results:
            results = requests.get(self.imdb_content % (
                imdbId, API_KEY)).json().get("tv_results")
            if not results:
                requests.get(self.imdb_content % (
                imdbId, API_KEY)).json().get("person_results")
        trailer = self._get_trailer(str(results[0].get("id")))
        return results[0].update({"trailer":trailer})
    def get(self, tmdbId):
        results = requests.get(self.single_detail % (
            "movie", tmdbId, API_KEY)).json()
          # we get success=False key only when no content is found
          # else on success isnot present
        if not results.get("success", True):
            results = requests.get(self.single_detail % (
                "tv", tmdbId, API_KEY)).json()
            imdb_id = requests.get(self.get_imdb_id % (
                "tv", tmdbId, API_KEY)).json()["imdb_id"]
        else:
            imdb_id = requests.get(self.get_imdb_id%("movie", tmdbId, API_KEY)).json()["imdb_id"]

        results.update({"imdb_id":imdb_id,"trailer":self._get_trailer(tmdbId),})
        return results
    def search(self,query):
        if query:
            results = requests.get(self.query_base_url % (
                    "movie", API_KEY, query.replace(" ", "+"))).json()["results"]
            results.extend(requests.get(self.query_base_url % (
                "tv", API_KEY, query.replace(" ", "+"))).json()["results"])
            return results
        return None
    def _get_trailer(self, tmdbid):
        trailers = requests.get(self.video_base_url%("movie", tmdbid, API_KEY)).json().get("results")
        if not trailers:
            if requests.get(self.video_base_url%("tv", tmdbid, API_KEY)).json().get("success",True):
                trailers = requests.get(self.video_base_url%("tv", tmdbid, API_KEY)).json()["results"]
        if trailers:
            return trailers[0].get("key")
        else:
            return None
    def get_casts(self,tmdbid):
        cast = namedtuple("cast",("name","image"))
        casts = requests.get(self.cast_base_url%("movie",tmdbid,API_KEY)).json()
        if not casts.get("success",True):
            casts = requests.get(self.cast_base_url%("tv",tmdbid,API_KEY)).json()

        filterd_casts = [cast(crew.get("original_name"),crew.get("profile_path")) for crew in casts.get("cast")]
        return filterd_casts
if __name__ == "__main__":
    tmdb = TMDBAPI()
    for movie in tmdb.search("hello"):
        print(movie)
