from socket import *
import os
import sys

"""
全局变量： 很多封装模块都要用，或者有一定的固定含义
"""


class ServerModel:
	"""
	服务端对象类
	"""
	def __init__(self):
		# 存储用户字典
		self.dict_user = {}
		# 创建套接字
		self.s = socket(AF_INET, SOCK_DGRAM)
		self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.pid = None
		self.ADDR = ("0.0.0.0", 9527)
		# 绑定地址
		self.s.bind(self.ADDR)

	def main(self):
		"""
		dup 服务端
		:return:
		"""
		self.pid = os.fork()
		if self.pid == 0:  # 子进程处理管理员消息
			while True:
				msg = input("manager MSG>: ")
				msg = "C manager " + msg
				self.s.sendto(msg.encode(), self.ADDR)
		else:
			# 请求处理函数
			self.do_request()

	def do_request(self):
		"""
		根据接收到的信息的第二个元素，做出不同处理
		"""
		while True:
			data, addr = self.s.recvfrom(1024)
			tmp = data.decode().split(" ")  # 拆分请求
			#  * 进入聊天室： L   * 聊天： C  * 退出： Q
			if tmp[0] == "L":
				self.do_login(tmp[1], addr)  # 执行具体工作
			elif tmp[0] == "C":
				text = " ".join(tmp[2:])
				self.do_chat(tmp[1], text)
			elif tmp[0] == 'Q':
				self.do_quit(tmp[1])

	def do_login(self, user_name, addr):
		"""
		登陆方法
		:param user_name: recvfrom(1024) 接收到的姓名
		:param addr: recvfrom(1024) 接收到的地址
		:return: None
		"""
		# manager 名称不能用来命名
		if user_name in self.dict_user or "manager" in user_name:
			self.s.sendto("this user has existed!".encode(), addr)
			return
		else:
			self.s.sendto(b"OK", addr)
			# 通知所有用户，有新人加入
			for ever in self.dict_user:
				self.s.sendto(f"\n{user_name} has entered the room， welcome~".encode(), self.dict_user[ever])
			# 存入用户字典
			self.dict_user[user_name] = addr
			return

	def do_chat(self, name, context):
		"""
		接收消息，处理后（改成姓名：内容形式），发送给其他用户
		:param s: 套接字
		:param name: 用户姓名
		:param context: 聊天内容
		:return: None
		"""
		context = "%s :" % str(name) + context
		for ever in self.dict_user:
			if ever != name:
				self.s.sendto(context.encode(), self.dict_user[ever])
		return

	def do_quit(self, name):
		"""
		向所有用户告知，用户已经离开
		:param name: 用户姓名
		:return: None
		"""
		quit_msg = "\n%s has left room~" % str(name)
		for ever in self.dict_user:
			self.s.sendto(quit_msg.encode(), self.dict_user[ever])
			if ever == name:
				self.s.sendto(b'EXIT', self.dict_user[ever])
		del self.dict_user[name]
		return


if __name__ == '__main__':
	s1 = ServerModel()
	s1.main()

