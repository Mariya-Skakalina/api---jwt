# Generated by Django 3.1.2 on 2020-10-20 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201020_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
