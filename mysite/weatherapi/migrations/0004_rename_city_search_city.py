# Generated by Django 5.0.7 on 2024-07-18 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('weatherapi', '0003_city_search_count_alter_city_search_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='city_search',
            new_name='City',
        ),
    ]
