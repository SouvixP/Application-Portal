# Generated by Django 3.0.2 on 2020-07-24 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200724_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='permission',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
