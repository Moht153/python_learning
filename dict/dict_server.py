"""
dict 服务端

功能：业务逻辑处理
模型：多进程tcp并发
"""

import socket
import multiprocessing
import signal
import sys
import time
from operation_db import *

# 全局变量
HOST = '127.0.0.1'
PORT = 9527
ADDR = (HOST, PORT)
db = DBOperation(database="dict")


def request(connfd, addr):
	db.create_cursor()
	"""循环地接收/发送客户端请求"""
	while True:
		data = connfd.recv(32).decode()

		print(connfd.getpeername(), ":", data)
		# 为什么要放到这里
		# 存在客户端异常退出，导致data为空，服务端报错
		# 避免此类情况，在此处加如判断
		if not data or data[0] == "E":
			# 子进程结束，关闭游标
			db.cur_close()
			print(addr, "has exited")
			return
		if data[0] == "R":
			# 调用数据库注册信息存入函数
			do_register(connfd, data)
		elif data[0] == "L":
			# 调用数据库注册信息存入函数
			do_login(connfd, data)
		elif data[0] == "Q":
			# 调用数据库，查询单词解释
			do_query(connfd, data)
		elif data[0] == "H":
			# 调用数据库，查询history表用户记录
			do_hist(connfd, data)


# # 调用查询单词函数
# answer = db_handle(data)
# if answer:
# 	connfd.send(answer.encode())
# 	connfd.close()
# else:
# 	connfd.send('单词不存在～'.encode())
# 	connfd.close()
# 	return


def do_register(connfd, data):
	data = data.strip().split(" ")
	print(data[1], data[2])
	name = data[1]
	passwd = data[2]
	answer = db.register(name, passwd)
	if answer:
		# 发送"OK"表示注册成功
		connfd.send(b"OK")
	else:
		# 发送"No"表示注册失败
		connfd.send(b"No")


def do_login(connfd, data):
	"""
	用户登陆
	:param connfd: 连接对象
	:param data: 用户传入信息
	:return: None
	"""
	data = data.strip().split(" ")
	print(data[1], data[2])
	name = data[1]
	passwd = data[2]
	answer = db.login(name, passwd)
	if answer == 2:
		# 发送"OK"表示注册成功
		connfd.send(b"OK")
	elif answer == 1:
		# 没有查询到该用户，返回提示信息
		connfd.send(b"NU")
	else:
		# 发送"No"表示注册失败
		connfd.send(b"No")


def do_query(connfd, data):
	"""
	单词查询
	:param connfd: 连接对象
	:param data: 用户传入信息
	:return:
	"""
	data = data.strip().split(" ")
	print(data[1])
	word = data[1]
	name = data[2]
	# 插入历史记录
	db.insert_history(name, word)

	# 没找到返回None, 找到返回单词解释
	mean = db.query(word)
	if mean:
		# 向客户端发送信息
		msg = "%s : %s" % (word, mean)
		connfd.send(msg.encode())
	else:
		connfd.send("单词不存在".encode())


def do_hist(connfd, data):
	"""
	执行查看历史记录功能
	查看最近查找的10条记录
	:param connfd: 连接对象
	:param data: 用户传入信息
	:return:
	"""
	data = data.strip().split(" ")
	name = data[1]
	response = db.do_hist(name)
	print("handle hist name")
	if not response:
		connfd.send("该用户还没有查询记录～".encode())
	else:
		for item in response:
			info = "name: %s\tword: %s\ttime: %s" % item
			connfd.send(info.encode())
		# 等待0.5s,确保下面要发的“##”跟上一条记录一块发了，俗称粘包
		time.sleep(0.1)
		connfd.send(b'##')

# 搭建网络
def main():
	# 创建TCP流式套接字
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 绑定地址
	s.bind(ADDR)
	# 监听
	s.listen(5)

	# 处理僵尸进程
	signal.signal(signal.SIGCHLD, signal.SIG_IGN)

	# 循环等待客户端连接
	print("Listen to the port 9527")
	while True:
		try:
			c, addr = s.accept()
			print("Connect from", addr)
		except KeyboardInterrupt:
			s.close()
			# 服务端退出时，退出数据库连接
			db.close()
			sys.exit("服务端退出")
		except Exception as e:
			print(e)
			continue

		# 为客户端创建子进程
		p = multiprocessing.Process(target=request, args=(c, addr))
		p.daemon = True
		p.start()
		# 此处如果服务端异常中途停止工作会报错
		try:
			p.join()
		except KeyboardInterrupt as e:
			print(e)
			sys.exit("服务端退出")


if __name__ == "__main__":
	main()
