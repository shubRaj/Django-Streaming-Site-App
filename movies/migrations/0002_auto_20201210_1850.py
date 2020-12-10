# Generated by Django 3.1.2 on 2020-12-10 18:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='production',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='uploaded_on',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
    ]
