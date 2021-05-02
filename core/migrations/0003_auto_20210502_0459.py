# Generated by Django 2.2 on 2021-05-02 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210502_0457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='features',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
