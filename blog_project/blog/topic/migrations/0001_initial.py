# Generated by Django 3.2.16 on 2022-12-30 07:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='文章标题')),
                ('category', models.CharField(max_length=20, verbose_name='文章分类')),
                ('limit', models.CharField(max_length=10, verbose_name='文章权限')),
                ('introduce', models.CharField(max_length=90, verbose_name='文章简介')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.userprofile')),
            ],
            options={
                'db_table': 'topic',
            },
        ),
    ]
