# Generated by Django 4.1.6 on 2023-02-24 08:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('reviews', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='trailreviews',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='touristreviews',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.guide'),
        ),
        migrations.AddField(
            model_name='touristreviews',
            name='tourist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.tourist'),
        ),
        migrations.AddField(
            model_name='guidereviews',
            name='guide',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.guide'),
        ),
        migrations.AddField(
            model_name='guidereviews',
            name='tourist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.tourist'),
        ),
        migrations.AddIndex(
            model_name='trailreviews',
            index=models.Index(fields=['trail', 'user'], name='reviews_tra_trail_i_33c565_idx'),
        ),
        migrations.AddConstraint(
            model_name='trailreviews',
            constraint=models.UniqueConstraint(fields=('trail', 'user'), name='unique_field_trail_user'),
        ),
        migrations.AddIndex(
            model_name='touristreviews',
            index=models.Index(fields=['guide', 'tourist'], name='reviews_tou_guide_i_9b8e36_idx'),
        ),
        migrations.AddConstraint(
            model_name='touristreviews',
            constraint=models.UniqueConstraint(fields=('guide', 'tourist'), name='unique_guide_tourist'),
        ),
        migrations.AddIndex(
            model_name='guidereviews',
            index=models.Index(fields=['tourist', 'guide'], name='reviews_gui_tourist_213325_idx'),
        ),
        migrations.AddConstraint(
            model_name='guidereviews',
            constraint=models.UniqueConstraint(fields=('tourist', 'guide'), name='unique_field_guide_tourist'),
        ),
    ]
