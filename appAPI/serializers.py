from rest_framework import serializers
from movies.models import Movie
from .models import AdsConfig,AppConfig,PaymentConfig,ApkVersionInfo
class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude=("uploaded_on","imdbID")
class AdsConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdsConfig
        exclude=("id",)
class AppConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppConfig
        exclude=("id",)
class PaymentConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentConfig
        exclude=("id",)
class ApkVersionInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApkVersionInfo
        exclude=("id",)