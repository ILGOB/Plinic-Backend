# Generated by Django 3.2.14 on 2022-07-31 17:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_profile_nickname'),
        ('plinic', '0003_alter_post_voter_set'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='voter_set',
            field=models.ManyToManyField(blank=True, related_name='voter_set', to='accounts.Profile'),
        ),
    ]
