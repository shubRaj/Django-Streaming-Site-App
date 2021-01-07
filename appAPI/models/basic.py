from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator
# Create your models here.
MENU_CHOICES = (
    ("vertical","VERTICAL"),
    ("grid","GRID"),
)
ADS_CHOICES = (
    ("admob","ADMOB"),
    ("fan","FACEBOOK_AUDIANCE NETWORK"),
    ("startapp","STARTAPP"),
)
ADS_ENABLE_CHOICES = (
    ("1","ENABLE"),
    ("0","DISABLE"),
)
CURRENCY_CHOICES=(
    ("$","USD"),
    ("₹","INR")
)
class AppConfig(models.Model):
    menu = models.CharField(choices=MENU_CHOICES,max_length=8,default="vertical")
    program_guide_enable = models.BooleanField(default=False)
    mandatory_login = models.BooleanField(default=False)
    genre_visible=models.BooleanField(default=True)
    country_visible = models.BooleanField(default=False)
    def save(self,*args,**kwargs):
        if not self.id and AppConfig.objects.exists():
            raise ValidationError(("Already Exists"),code="invalid")
        return super().save(*args,**kwargs)
    class Meta:
        verbose_name_plural= "APP Configuration"
class AdsConfig(models.Model):
    ads_enable = models.CharField(choices=ADS_ENABLE_CHOICES,max_length=1,default='1')
    mobile_ads_network = models.CharField(choices=ADS_CHOICES,max_length=8,default='admob')
    admob_app_id = models.CharField(max_length=200,blank=True,null=True)
    admob_banner_ads_id = models.CharField(max_length=200,blank=True,null=True)
    admob_interstitial_ads_id = models.CharField(max_length=200,blank=True,null=True)
    fan_native_ads_placement_id = models.CharField(max_length=200,blank=True,null=True)
    fan_banner_ads_placement_id = models.CharField(max_length=200,blank=True,null=True)
    fan_interstitial_ads_placement_id = models.CharField(max_length=200,blank=True,null=True)
    startapp_app_id = models.CharField(max_length=200,blank=True,null=True)
    def save(self,*args,**kwargs):
        if not self.id and AdsConfig.objects.exists():
            raise ValidationError(("Already Exists"),code="invalid")
        return super().save(*args,**kwargs)
    class Meta:
        verbose_name_plural= "Advertisement Configuration"
class PaymentConfig(models.Model):
    currency_symbol = models.CharField(max_length=4,default="$")
    currency = models.CharField(max_length=8,blank=True)
    exchnage_rate = models.IntegerField(validators=[MaxValueValidator(5000),],default=1)
    paypal_enable = models.BooleanField(default=False)
    paypal_email = models.EmailField(max_length=30,default="john@cena.com")
    paypal_client_id = models.CharField(blank=True,max_length=200,null=True)
    stripe_enable = models.BooleanField(default=False)
    stripe_publishable_key = models.CharField(max_length=200,blank=True,null=True)
    stripe_secret_key = models.CharField(max_length=200,blank=True,null=True)
    razorpay_enable= models.BooleanField(default=False)
    razorpay_key_id = models.CharField(max_length=200,null=True,blank=True)
    razorpay_key_secret =models.CharField(max_length=200,null=True,blank=True)
    razorpay_inr_exchange_rate = models.IntegerField(validators=[MaxValueValidator(5000),],default=1)
    def save(self,*args,**kwargs):
        if not self.id and PaymentConfig.objects.exists():
            raise ValidationError(("Already Exists"),code="invalid")
        return super().save(*args,**kwargs)
    class Meta:
        verbose_name_plural= "Payment configuration"
class ApkVersionInfo(models.Model):
    version_code = models.CharField(max_length=3,default="30")
    version_name = models.CharField(max_length=6,default="v1.0.0")
    whats_new = models.TextField()
    apk_url = models.URLField()
    is_skipable = models.BooleanField(default=True)
    class Meta:
        verbose_name_plural= "APK Version Information"