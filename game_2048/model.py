"""
	数据模型
"""


class DirectionModel:
	"""
		方向数据模型
		枚举
	"""
	# 在整数的基础上，添加一个人容易识别的“标签”
	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3


class Location:
	def __init__(self, r, c):
		self.r_index = r
		self.c_index = c