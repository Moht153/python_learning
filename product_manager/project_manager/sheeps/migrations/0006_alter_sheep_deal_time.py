# Generated by Django 3.2.16 on 2023-01-08 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheeps', '0005_sheep_deal_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheep',
            name='deal_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
