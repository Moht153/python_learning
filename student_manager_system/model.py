"""
	定义数据模型
"""


class StudentModel:
	"""
	数据模型类 StudentModel
	"""

	def __init__(self, name="", age=0, score=0, id=0):
		"""
			创建学生对象
		:param id: 编号（该学生对象的唯一标识）
		:param name: 姓名    类型：str
		:param age: 年龄		类型：int
		:param score: 分数	类型：int
		"""
		self.id = id
		self.name = name
		self.age = age
		self.score = score
		self.dict_stu = {"id": self.id, "name": self.name, "age": self.age, "score": self.score}
