# Generated by Django 3.0.2 on 2020-07-24 20:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200725_0132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='author',
        ),
        migrations.RemoveField(
            model_name='staffhistory',
            name='author',
        ),
        migrations.DeleteModel(
            name='StudentHistory',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='StaffHistory',
        ),
    ]
