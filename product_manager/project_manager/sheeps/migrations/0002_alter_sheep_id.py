# Generated by Django 3.2.16 on 2023-01-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sheeps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheep',
            name='id',
            field=models.IntegerField(auto_created=True, primary_key=True, serialize=False, verbose_name='编号'),
        ),
    ]
