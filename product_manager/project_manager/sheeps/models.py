from django.db import models

# Create your models here.

class Sheep(models.Model):
	id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='编号')
	weight = models.FloatField(max_length=5, null=True, verbose_name='羊肉重量（千克）')


	class Meta:
		db_table = 'sheeps'