# Generated by Django 4.1.6 on 2023-02-23 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0007_trail_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='guidetrail',
            name='money_rate',
            field=models.FloatField(default=1000),
        ),
    ]
