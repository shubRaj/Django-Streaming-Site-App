# Generated by Django 3.1.2 on 2020-12-10 19:10

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20201210_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('en', 'ENGLISH'), ('hi', 'HINDI'), ('ch', 'CHINESE'), ('pun', 'PUNJABI')], max_length=30, null=True),
        ),
    ]