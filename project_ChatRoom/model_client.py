"""
chat room 客户端
发送请求，展示结果
* 进入聊天室：
	客户端：
	 1 ：输入姓名
	 2 ：将请求发送给服务器
	 3 ： 接收结果
	 4 ： 允许则可以聊天，不允许则重新输入姓名
* 聊天
	客户端：
	* 创建新的进程
	* 一个进程循环发送消息
	* 一个进程循环接收消息

* 退出聊天室
	客户端：
	* 输入quit 或者ctrl+c 退出
	* 将请求发送给服务端
	* 结束进程
	* 客户端受到 "EXIT"结束接收进程
"""
import os
import sys
from socket import *


class ClientModel:
	"""
	聊天室客户端对象类
	"""
	def __init__(self):
		# 服务器地址
		self.ADDR = ("192.168.40.130", 9527)
		# 创建套接字
		self.s = socket(AF_INET, SOCK_DGRAM)
		self.pid = None
		self.pid01 = None  # 二级子进程

	# 客户端启动函数
	def main(self):
		"""
		dup 客户端
		:return:
		"""
		# 进入聊天室
		while True:
			name = input("plz input name:\n")
			msg = "L " + name
			self.s.sendto(msg.encode(), self.ADDR)
			# 接收反馈
			data, addr = self.s.recvfrom(1024)
			if addr == self.ADDR and data == b"OK":
				print("Welcome! U have entered the room")
				break
			else:
				print("plz enter other name(name U put is used by others!)")
				continue

		# 已经进入聊天室
		self.pid = os.fork()

		if self.pid == 0:
			self.pid01 = os.fork()
			if self.pid01 == 0:  # 子进程负责接收消息
				# 接收消息并返回一个布尔值
				self.recv_msg()

			sys.exit(1)

		elif self.pid > 0:
			os.wait()
			print("let's talk~")
			# 父进程负责发消息
			self.send_msg(name)

	def recv_msg(self):
		"""
		接收消息
		:return: 如果服务端返回'EXIT'，则返回一个True
		"""
		while True:
			try:
				# 接收反馈
				data, addr = self.s.recvfrom(1024)
			except KeyboardInterrupt:
				sys.exit("sub_process is end, Bye~")
			else:
				context = data.decode()
				if addr == self.ADDR:
					# 从服务器收到EXIT 退出
					if context == 'EXIT':
						sys.exit("sub_process is end, Bye~")
					else:
						print(context + '\nmsg>:', end='')

	def send_msg(self, name):
		"""
		发送消息
		:param name: 开始输入的用户名称
		:return: None
		"""
		while True:
			try:
				msg = input("msg>:")
			except KeyboardInterrupt:
				msg = 'quit'
			if msg.strip() == "quit":
				msg = "Q %s" % name
				self.s.sendto(msg.encode(), self.ADDR)
				break

			else:
				msg = "C %s %s" % (name, msg)
				self.s.sendto(msg.encode(), self.ADDR)


if __name__ == '__main__':
	c1 = ClientModel()
	c1.main()