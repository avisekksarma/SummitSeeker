
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hire', '0003_trail_mapimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hire',
            name='status',
            field=models.CharField(choices=[('RQ', 'Requested'), ('AC', 'Accepted'), ('RJ', 'Rejected'), ('HR', 'Hired')], max_length=2),
        ),
    ]
