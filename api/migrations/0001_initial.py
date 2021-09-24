# Generated by Django 3.2.7 on 2021-09-24 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=255)),
                ('weather_main', models.CharField(max_length=50)),
                ('weather_desc', models.CharField(max_length=255)),
                ('temp', models.FloatField()),
                ('pressure', models.FloatField()),
                ('humidity', models.FloatField()),
                ('visibility', models.FloatField()),
                ('wind_speed', models.FloatField()),
            ],
        ),
    ]
