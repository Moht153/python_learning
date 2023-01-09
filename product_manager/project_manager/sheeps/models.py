from django.db import models

# Create your models here.


class Sheep(models.Model):
	id = models.IntegerField(primary_key=True, auto_created=True, verbose_name='编号')
	weight = models.FloatField(max_length=5, null=True, verbose_name='羊肉重量（千克）')
	real_weight = models.FloatField(max_length=5, null=True, verbose_name='羊肉实际重量（千克）')
	customer = models.CharField(max_length=16, null=True, verbose_name='顾客姓名')
	single_price = models.FloatField(max_length=8, null=True, verbose_name='单价 元/kg')
	total_price = models.FloatField(max_length=8, null=True, verbose_name='总价 元')
	memo = models.CharField(max_length=100, null=True, verbose_name='备注')
	deal_date = models.DateTimeField(auto_now=True, null=True)  # 修改时加入时间

	class Meta:
		db_table = 'sheeps'