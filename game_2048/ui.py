import os

from bll import GameCoreController
from model import DirectionModel


class GameConsoleView:
	"""
		2048 游戏UI
	"""

	def __init__(self):
		self.__controller = GameCoreController()
		self.__input_charge = False

	def __start(self):
		# 产生两数字
		self.__controller.generate_new_number()
		self.__controller.generate_new_number()
		# 绘制界面
		self.__draw_map()

	def __draw_map(self):
		os.system('clear')
		self.__controller.show_rectangle()

	@staticmethod
	def __display_menu():
		print("4)向左", end=" ")
		print("6)向右", end=" ")
		print("8)向上", end=" ")
		print("2)向下")

	def __move_map_from_input(self):
		dic_dir = {
			"w": DirectionModel.UP,
			"s": DirectionModel.DOWN,
			"a": DirectionModel.LEFT,
			"d": DirectionModel.RIGHT
				   }

		item = input("请输入方向（wsad,退出：q）：")
		if item == "q":
			return True
		elif item in ("w", "s", "a", "d"):
			self.__controller.move(dic_dir[item])
			return False
		elif item in dic_dir:
			print("无法识别输入内容~")
			return False

	def __update(self):
		while True:
			# 循环
			# 判断玩家的输入 --> 移动地图
			self.__input_charge = self.__move_map_from_input()
			# 产生新数字
			self.__controller.generate_new_number()
			# 绘制界面
			self.__draw_map()
			# 游戏结束判断 --> 提示
			if self.__controller.is_game_end() or self.__input_charge:
				print("~Game Over~")
				break

	def main(self):
		self.__start()
		self.__update()

