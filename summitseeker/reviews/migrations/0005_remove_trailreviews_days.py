# Generated by Django 4.1.6 on 2023-02-23 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_alter_trailreviews_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trailreviews',
            name='days',
        ),
    ]
