# Generated by Django 4.1.6 on 2023-02-19 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_alter_user_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='language',
            field=models.ManyToManyField(blank=True, default=['EN'], to='user.language'),
        ),
    ]
