"""
dict 服务端

功能：业务逻辑处理
模型：多进程tcp并发
"""

import socket
import multiprocessing
import signal
import sys
from operation_db import *

# 全局变量
HOST = '127.0.0.1'
PORT = 9527
ADDR = (HOST, PORT)
db = DBOperation(database="dict")


def request(connfd):
	db.create_cursor()
	"""循环地接收/发送客户端请求"""
	while True:
		data = connfd.recv(32).decode()
		print(connfd.getpeername(), ":", data)
		if data[0] == "R":
			# 调用数据库注册信息存入函数
			do_register(connfd, data)
	# 子进程结束，关闭游标
	db.cur_close()


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
	# name = data[1]
	# passwd = data[2]
	answer = db.register(data[1], data[2])
	if answer:
		# 发送"OK"表示注册成功
		connfd.send(b"OK")
	else:
		# 发送"No"表示注册失败
		connfd.send(b"No")


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
		p = multiprocessing.Process(target=request, args=(c,))
		p.daemon = True
		p.start()
		p.join()


if __name__ == "__main__":
	main()
