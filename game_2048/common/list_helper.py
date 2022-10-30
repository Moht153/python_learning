"""
	列表助手模块
"""


class ListHelper:
	"""
		列表助手类
	"""

	@staticmethod
	def find_all(list_target, func):
		"""
			通用的查找某个条件的所有元素方法
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return bool
		:param list_target: 需要查找的列表
		:return: 需要查找的元素,生成器类型
		"""
		for item in list_target:
			# “多态”思想
			# 执行：具体条件的函数：func(item)
			if func(item):
				yield item

	@staticmethod
	def find_one(list_target, func):
		"""
			通用的查找某个条件的单个元素方法
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return bool
		:param list_target: 需要查找的列表
		:return: 需要查找的元素,不是生成器，只返回一个值
		"""
		for item in list_target:
			# “多态”思想
			# 执行：具体条件的函数：func(item)
			if func(item):
				return item

	@staticmethod
	def get_number(list_target, func):
		"""
			通用的 计算 满足某个条件的 元素总数 的方法
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return bool
		:param list_target: 需要查找的列表
		:return: 需要查找的元素,不是生成器，只返回一个值
		"""
		count = 0
		for item in list_target:
			# “多态”思想
			# 执行：具体条件的函数：func(item)
			if func(item):
				count += 1
		return count

	@staticmethod
	def charge(list_target, func):
		"""
			判断列表中是否有满足条件的元素
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return bool
		:param list_target: 需要查找的列表
		:return: 只返回一个 bool值  存在：True/ 不存在：False
		"""
		for item in list_target:
			# “多态”思想
			# 执行：具体条件的函数：func(item)
			if func(item):
				return True
		return False

	@staticmethod
	def get_sum(list_target, func):
		"""
			计算列表中满足要求的元素值的总和，数值累加运算
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return int
		:param list_target: 需要查找的列表
		:return: 返回一个 变量，类型：int
		"""
		sum_value = 0
		for item in list_target:
			# 执行：具体条件的函数：func(item)
			sum_value += func(item)
		return sum_value

	@staticmethod
	def get_list(list_target, func):
		"""
			通用的筛选方法，返回指定的满足要求的信息列表
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return 变量
		:param list_target: 需要查找的列表
		:return: 返回一个 列表 或者元祖（可以修改）
		"""
		list_require = []
		for item in list_target:
			# 执行：具体条件的函数：func(item)
			list_require.append(func(item))
		return tuple(list_require)

	@staticmethod
	def get_info(list_target, func):
		"""
			通用的筛选方法，依次返回（yield）指定的满足要求的信息容器（变量、列表、元祖）
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> return int/str/tuple/list其他类型的变量（任意类型的变量）
		:param list_target: 需要查找的列表
		:return: 生成器类型，配合for使用，返回一个数据
		"""
		for item in list_target:
			# 执行：具体条件的函数：func(item)
			yield func(item)

	@staticmethod
	def get_max(list_target, func):
		"""
			通用的筛选方法，返回列表中某一属性最大的对象
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> 对象属性（int类型）
		:param list_target: 需要查找的列表
		:return: 返回一个对象
		"""
		the_most_one = list_target[0]
		for index in range(1, len(list_target)):
			if func(the_most_one) <= func(list_target[index]):
				the_most_one = list_target[index]
		return the_most_one

	@staticmethod
	def get_min(list_target, func):
		"""
			通用的筛选方法，返回列表中某一属性最小的对象
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> 对象属性（int类型）
		:param list_target: 需要查找的列表
		:return: 返回一个对象
		"""
		the_most_one = list_target[0]
		for index in range(1, len(list_target)):
			if func(the_most_one) >= func(list_target[index]):
				the_most_one = list_target[index]
		return the_most_one

	@staticmethod
	def order_by_asc(list_target, func):
		"""
			将列表元素按照要求属性进行升序排序
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> 对象属性（int/float ...需要比较的类型）
		:param list_target: 需要排序的列表
		:return: 没有返回值，只改变了列表元素排列顺序
		"""
		for r in range(len(list_target) - 1):
			for c in range(r + 1, len(list_target)):
				if func(list_target[r]) > func(list_target[c]):
					list_target[r], list_target[c] = list_target[c], list_target[r]

	@staticmethod
	def order_by_desc(list_target, func):
		"""
			将列表元素按照要求属性进行降序排序
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> 对象属性（int/float ...需要比较的类型）
		:param list_target: 需要排序的列表
		:return: 没有返回值，只改变了列表元素排列顺序
		"""
		for r in range(len(list_target) - 1):
			for c in range(r + 1, len(list_target)):
				if func(list_target[r]) < func(list_target[c]):
					list_target[r], list_target[c] = list_target[c], list_target[r]

	@staticmethod
	def del_require_unit(list_target, func):
		"""
			通用的，根据条件，删除数据容器中指定的对象
		:param list_target: 目标列表
		:param func: 需要查找的条件，函数类型
				函数名(参数) --> True/False Bool类型
		"""
		for index in range(len(list_target) - 1, -1, -1):
			if func(list_target[index]):
				print(list_target[index].name, "已删除")
				del list_target[index]

	@staticmethod
	def rectangle_exchange(list_target):
		"""
			矩阵转置
		:param list_target: 目标列表
		"""
		list_handle = []
		for c in range(len(list_target[0])):
			list_handle.append([])
			for r in range(len(list_target)):
				list_handle[c].append(list_target[r][c])
		list_target[:] = list_handle

	@staticmethod
	def find01(item):
		return item.name == "葵花宝典"

	@staticmethod
	def find02(item):
		return item.id == 101

	# 案例：查找最先满足持续时间大于0的技能
	@staticmethod
	def find03(item):
		return item.duration > 0
