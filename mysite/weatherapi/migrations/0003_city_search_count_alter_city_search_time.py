# Generated by Django 5.0.7 on 2024-07-18 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapi', '0002_city_search_latitude_city_search_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='city_search',
            name='count',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='city_search',
            name='time',
            field=models.DateField(auto_now=True),
        ),
    ]
