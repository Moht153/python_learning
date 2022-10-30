"""
	界面代码
"""
from bll import StudentManagerController
from model import StudentModel


class StudentManagerView:
	"""
		学生视图系统
	"""

	def __init__(self):
		self.__manager = StudentManagerController()

	@staticmethod
	def __display_menu():
		print("1)添加学生")
		print("2)显示学生")
		print("3)删除学生")
		print("4)修改学生")
		print("5)按照成绩升序显示学生")

	def __select_menu(self):
		item = input("请输入：")
		if item == "1":
			self.__input_student()
		elif item == "2":
			self.__output_students()
		elif item == "3":
			self.__delete_student()
		elif item == "4":
			self.__modify_student()
		elif item == "5":
			self.__show_order_by_score()
		elif item == "":
			print("---end---")
			return True
		else:
			print("无法识别输入内容~")

	def main(self):
		if_out = None
		while not if_out:
			self.__display_menu()
			if_out = self.__select_menu()

	@staticmethod
	def __input_parameter(message):
		while True:
			try:
				parameter = int(input(message))
				return parameter
			except ValueError:
				print("输入有误！请重新输入")


	def __input_student(self):
		name = input("请输入姓名：\n")

		age = self.__input_parameter("请输入年龄：\n")

		score = self.__input_parameter("请输入成绩：\n")
		stu = StudentModel(name, age, score, id=0)
		self.__manager.add_student(stu.dict_stu)

	def __output_students(self):
		self.__manager.print_stu_list()

	def __delete_student(self):
		id = self.__input_parameter("输入要删除的学生id：\n")
		if self.__manager.remove_student(id):
			print("移除成功")
		else:
			print("id不在名单中")

	def __modify_student(self):
		stu = StudentModel(name=input("请输入新的学生姓名：\n"), age=self.__input_parameter("请输入新的学生年龄：\n"),
						   score=self.__input_parameter("请输入新的学生成绩：\n"), id=self.__input_parameter("输入id：\n"))
		if self.__manager.update_student(stu):
			print("\n修改成功\n")
		else:
			print("\nid不在名单中\n")

	def __show_order_by_score(self):
		self.__manager.order_by_score()
		self.__manager.print_stu_list()
