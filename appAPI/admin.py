from django.contrib import admin
from .models import AdsConfig,AppConfig,PaymentConfig,ApkVersionInfo
admin.site.register([AdsConfig,AppConfig,PaymentConfig,ApkVersionInfo])
# Register your models here.
