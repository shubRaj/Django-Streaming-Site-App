# Generated by Django 3.1.2 on 2020-12-13 18:04

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0029_auto_20201213_1648'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='category',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('action', 'ACTION'), ('drama', 'DRAMA'), ('comedy', 'COMEDY'), ('romance', 'ROMANCE'), ('adventure', 'ADVENTURE'), ('animation', 'ANIMATION'), ('crime', 'CRIME'), ('documentary', 'DOCUMENTARY'), ('family', 'FAMILY'), ('fantasy', 'FANTASY'), ('horror', 'HORROR'), ('music', 'MUSIC'), ('scifi', 'SCI-FI'), ('thriller', 'THRILLER'), ('war', 'WAR')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='language',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('en', 'ENGLISH'), ('hi', 'HINDI'), ('ch', 'CHINESE'), ('pun', 'PUNJABI')], max_length=100, null=True),
        ),
    ]