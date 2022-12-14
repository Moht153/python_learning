# Generated by Django 3.2.16 on 2023-01-07 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('username', models.CharField(max_length=11, primary_key=True, serialize=False, verbose_name='用户姓名')),
                ('email', models.CharField(max_length=50, null=True, verbose_name='邮箱')),
                ('password', models.CharField(max_length=32)),
                ('avatar', models.ImageField(upload_to='avatar/')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
