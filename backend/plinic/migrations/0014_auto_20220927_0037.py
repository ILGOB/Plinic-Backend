# Generated by Django 3.2.14 on 2022-09-27 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("plinic", "0013_alter_playlist_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notice",
            name="title",
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name="playlist",
            name="title",
            field=models.CharField(default="tempList", max_length=30),
        ),
        migrations.AlterField(
            model_name="track",
            name="title",
            field=models.CharField(max_length=30),
        ),
    ]
