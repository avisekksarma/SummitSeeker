# Generated by Django 4.1.6 on 2023-02-23 09:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0008_guidetrail_money_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hire',
            name='deadline',
            field=models.IntegerField(),
        ),
    ]