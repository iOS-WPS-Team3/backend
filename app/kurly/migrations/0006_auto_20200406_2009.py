# Generated by Django 2.2.12 on 2020-04-06 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kurly', '0005_auto_20200406_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='summary',
            field=models.CharField(blank=True, max_length=70),
        ),
    ]