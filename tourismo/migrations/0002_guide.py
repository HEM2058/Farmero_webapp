# Generated by Django 4.2 on 2023-04-29 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tourismo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('contact', models.CharField(max_length=50)),
                ('sex', models.CharField(max_length=50)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
        ),
    ]
