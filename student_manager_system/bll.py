"""
	业务逻辑处理
"""


class StudentManagerController:
	"""
		学生管理控制器 StudentManagerController
		作用：负责业务逻辑处理
	"""
	# 类变量，初始编号
	__init_id = 1000

	def __init__(self):
		self.__stu_list = []

	@property
	def stu_list(self):
		"""
			学生列表
		:return: 返回 self.__stu_list
		"""
		return self.__stu_list

	def add_student(self, dic_add):
		"""
			添加学生信息
		:param dic_add:	学生信息		类型：字典
		"""
		dic_add["id"] = self.id_generator()
		self.stu_list.append(dic_add)

	@staticmethod
	def id_generator():
		"""
			更新学生id（类变量）
		"""
		StudentManagerController.__init_id += 1
		return StudentManagerController.__init_id

	# def remove_student(self, stu_id):
	# 	for i in range(len(self.stu_list) - 1, -1, -1):
	# 		if self.stu_list[i]["id"] == stu_id:
	# 			del self.stu_list[i]
	# 			return True  # 移除成功
	# 	return False  # 移除失败
	#
	def remove_student(self, stu_id):
		for dict01 in self.stu_list:
			if dict01["id"] == stu_id:
				self.stu_list.remove(dict01)
				return True  # 移除成功
		return False  # 移除失败

	def update_student(self, stu_info):
		"""
			修改学生信息
		:param stu_info:修改后的学生对象
		:return: 修改状态 	True，False
		"""
		for i in range(len(self.stu_list)):
			if self.stu_list[i]["id"] == stu_info.id:
				print("修改前学生id：%s\t学生姓名：%s\t年龄：%s\t分数：%s"
					  % (self.stu_list[i]["id"], self.stu_list[i]["name"],
						 self.stu_list[i]["score"], self.stu_list[i]["age"]))
				self.__stu_list[i] = stu_info.dict_stu
				print("修改后学生id：%s\t学生姓名：%s\t年龄：%s\t分数：%s"
					  % (self.stu_list[i]["id"], self.stu_list[i]["name"],
						 self.stu_list[i]["score"], self.stu_list[i]["age"]))
				return True  # 修改成功
		return False  # 修改失败

	def print_stu_list(self):
		for item in self.__stu_list:
			print("id:%s\t name:%s\t age:%d\t score:%d" \
				  % (item["id"], item["name"], item["age"], item["score"]))

	def order_by_score(self):
		for r in range(len(self.__stu_list) - 1):
			for c in range(r + 1, len(self.__stu_list)):
				if self.__stu_list[r]["score"] > self.__stu_list[c]["score"]:
					self.__stu_list[r], self.__stu_list[c] = self.__stu_list[c], self.__stu_list[r]
