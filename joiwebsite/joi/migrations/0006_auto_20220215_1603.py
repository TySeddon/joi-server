# Generated by Django 3.2.11 on 2022-02-15 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('joi', '0005_auto_20220211_1925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediainteraction',
            name='carepartner_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mediainteraction',
            name='researcher_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='memoryboxsessionmedia',
            name='carepartner_flag',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='memoryboxsessionmedia',
            name='researcher_flag',
            field=models.BooleanField(default=False),
        ),
    ]
