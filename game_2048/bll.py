"""
	游戏逻辑控制器：2048 游戏核心算法
"""
import random

from model import DirectionModel
from model import Location


class GameCoreController:

	def __init__(self):
		self.__map = [
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0],
		[0, 0, 0, 0]
	]
		self.__list_merge = []
		self.list_gen = []

	@property
	def list_map(self):
		return self.__map

	def show_rectangle(self):
		"""
			显示矩阵
		"""
		for item in self.__map:
			print()
			for unit in item:
				print("%2d\t" % unit, end="")
		print("\n")

	def __map_exchange(self):
		"""
			将矩阵转置
		:return:
		"""
		map_02 = []
		for c in range(len(self.__map[0])):
			map_02.append([])
			for r in range(len(self.__map)):
				map_02[c].append(self.__map[r][c])
		self.__map[:] = map_02

	def __zero_to_end(self):
		"""
			零元素移动到末尾
		"""

		for i in range(-1, -len(self.__list_merge) - 1, -1):
			if self.__list_merge[i] == 0:
				del self.__list_merge[i]
				self.__list_merge.append(0)

	def __merge_number(self):
		"""
			合并每一行中相同的元素
		:return:
		"""
		self.__zero_to_end()
		for i in range(0, len(self.__list_merge) - 1):
			if self.__list_merge[i] == self.__list_merge[i + 1]:
				self.__list_merge[i] += self.__list_merge[i + 1]
				del self.__list_merge[i + 1]
				self.__list_merge.append(0)

	def __move_left(self):
		"""
			左移
		:return:
		"""
		for i in range(len(self.__map)):
			self.__list_merge = self.__map[i]
			self.__merge_number()

	def __move_right(self):
		"""
			右移
		:return:
		"""
		for line in self.__map:
			self.__list_merge = line[::-1]
			self.__merge_number()
			line[:] = self.__list_merge[::-1]

	def __move_up(self):
		self.__map_exchange()
		self.__move_left()
		self.__map_exchange()

	def __move_down(self):
		self.__map_exchange()
		self.__move_right()
		self.__map_exchange()

	def move(self, direction):
		"""
			移动
		:param direction: DirectionModel 类变量
		"""
		if direction == DirectionModel.UP:
			self.__move_up()
		elif direction == DirectionModel.DOWN:
			self.__move_down()
		elif direction == DirectionModel.LEFT:
			self.__move_left()
		elif direction == DirectionModel.RIGHT:
			self.__move_right()

	def generate_new_number(self):
		"""
			按照概率产生整数 2 或者 4
			2 --> 90%
			4 --> 10%
		:return:
		"""
		self.get_empty_location()
		# 没有空位置，不产生新的数，return退出方法
		if len(self.list_gen) == 0:
			return
		# 这里loc实际为Location类对象，含有（r_index，loc.c_index）
		loc = random.choice(self.list_gen)
		# if random.randint(0, 9) == 1:
		# 	generate_number = 4
		# else:
		# 	generate_number = 2
		# self.__map[loc.r_index][loc.c_index] = generate_number
		# 提取出来做一个推导式
		self.__map[loc.r_index][loc.c_index] = 4 if random.randint(0, 9) == 1 else 2
		# 此处特别注意，为了防止self.list_gen只剩下1个时，补充数字后，系统检测游戏结束的尴尬局面
		self.list_gen.remove(loc)

	def get_empty_location(self):
		"""
			方法，找到二维列表中，数值是“0”的元素位置
		:return: self.list_gen:一个包含含有位置Location类对象的列表
		"""
		self.list_gen.clear()
		for r in range(len(self.__map)):
			for c in range(len(self.__map[0])):
				if self.__map[r][c] == 0:
					# 记录i，j --> 元祖
					self.list_gen.append(Location(r, c))

	def is_game_end(self):
		"""
			游戏是否结束？
		:return: True: 结束
				False: 未结束
		"""
		# 先找是否有空位
		self.get_empty_location()
		if len(self.list_gen) > 0:
			return False
		# 判断最后一行，同行不同列元素是否相同
		# last_row = self.__map[len(self.__map) - 1]
		# for cal in range(len(last_row) - 1):
		# 	if last_row[cal] == last_row[cal + 1]:
		# 		return False
		# # 循环每一行，判断每个元素与周围元素（下一行元素、下一列元素）是否相同
		# # 最后一行没有被循环，单独做出来进行与下一列元素进行比较
		# for row in range(len(self.__map)-1):
		# 	for cal in range(len(self.__map[row])-1):
		# 		# 比较同行下一列元素
		# 		if self.__map[row][cal] == self.__map[row][cal+1]:
		# 			return False
		# 		# 比较同列下一行元素
		# 		elif self.__map[row][cal] == self.__map[row + 1][cal]:
		# 			return False
		# return True

		# ---------------------------------------------------------------------------------
		# for row in range(len(self.__map)):
		# 	for cal in range(len(self.__map[row])-1):
		# 		# 比较同行下一列元素
		# 		if self.__map[row][cal] == self.__map[row][cal+1]:
		# 			return False
		#
		# for cal in range(len(self.__map[0])):
		# 	for row in range(len(self.__map)-1):
		# 		# 比较同行下一列元素
		# 		if self.__map[row][cal] == self.__map[row+1][cal]:
		# 			return False
		# 找共性，根据两个for循环结构上的相似性，最后总结出写法如下：
		for row in range(len(self.__map)):
			for cal in range(len(self.__map[row])-1):
				# 比较同行下一列元素
				if self.__map[row][cal] == self.__map[row][cal+1] or \
					self.__map[cal][row] == self.__map[cal + 1][row]:
					return False

if __name__ == "__main__":
	gm01 = GameCoreController()
	gm01.show_rectangle()
	print("-"*65)

	gm01.generate_new_number()

	gm01.show_rectangle()
	print(gm01.is_game_end())

