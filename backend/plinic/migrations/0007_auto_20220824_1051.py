# Generated by Django 3.2.14 on 2022-08-24 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("plinic", "0006_alter_playlist_thumbnail"),
    ]

    operations = [
        migrations.RenameField(
            model_name="playlist",
            old_name="url",
            new_name="total_url",
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(max_length=150)),
                ("url", models.URLField()),
                ("duration", models.DurationField()),
                (
                    "playlist",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="plinic.playlist",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
