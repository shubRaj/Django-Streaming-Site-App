# Generated by Django 3.1.2 on 2020-12-11 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0019_auto_20201211_0612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='production',
            field=models.DateField(blank=True, null=True),
        ),
    ]