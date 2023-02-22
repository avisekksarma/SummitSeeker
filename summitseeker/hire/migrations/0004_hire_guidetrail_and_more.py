# Generated by Django 4.1.6 on 2023-02-22 16:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_guide_reviews_tourist_reviews'),
        ('hire', '0003_remove_trail_average_days_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hire',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('deadline', models.DateField()),
                ('status', models.CharField(choices=[('RQ', 'Requested'), ('AC', 'Accepted'), ('RJ', 'Rejected'), ('NG', 'Negotiate'), ('HR', 'Hired')], max_length=2)),
                ('money_rate', models.FloatField()),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.guide')),
                ('tourist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.tourist')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hire.trail')),
            ],
        ),
        migrations.CreateModel(
            name='GuideTrail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guide', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.guide')),
                ('trail', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hire.trail')),
            ],
        ),
        migrations.AddIndex(
            model_name='guidetrail',
            index=models.Index(fields=['guide', 'trail'], name='hire_guidet_guide_i_305660_idx'),
        ),
        migrations.AddConstraint(
            model_name='guidetrail',
            constraint=models.UniqueConstraint(fields=('guide', 'trail'), name='unique_field_guide_trail'),
        ),
    ]
