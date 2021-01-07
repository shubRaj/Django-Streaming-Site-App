# Generated by Django 3.1.2 on 2020-12-20 09:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TorrentKeyword',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keyword', models.CharField(max_length=250, unique=True)),
                ('added_on', models.DateField(auto_now=True)),
            ],
            options={
                'ordering': ['-added_on'],
            },
        ),
        migrations.CreateModel(
            name='Magnet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=2083)),
                ('category', models.CharField(max_length=30)),
                ('seeders', models.IntegerField(default=0)),
                ('leechers', models.IntegerField(default=0)),
                ('size', models.CharField(blank=True, max_length=10, null=True)),
                ('magnet', models.TextField(null=True)),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('torrent', models.ManyToManyField(related_name='torrent_magnet', to='torrents.TorrentKeyword')),
            ],
            options={
                'ordering': ['-seeders', '-leechers'],
            },
        ),
    ]
