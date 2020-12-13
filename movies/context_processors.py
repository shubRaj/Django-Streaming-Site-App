from .models import CATEGORY_CHOICES,LANGUAGE_CHOICES,StaticTag
import datetime
def choices(request):
    year_today = datetime.datetime.now().year
    years = [year_today-backToPast for backToPast in range(10)]
    return {"category_choices":CATEGORY_CHOICES,"language_choices":LANGUAGE_CHOICES,"year_choices":years,
    "static_tags":StaticTag.objects.all()}