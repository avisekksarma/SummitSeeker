# Generated by Django 4.1.6 on 2023-02-24 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trail',
            name='mapImage',
            field=models.ImageField(blank=True, max_length=200, null=True, upload_to='trailphotos/mapImage/'),
        ),
    ]
