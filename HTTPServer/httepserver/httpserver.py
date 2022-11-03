"""
HTTPServer 部分的主程序：

获取http请求
解析http请求
将请求发送给WebFrame
从WebFrame接收反馈数据
将数据组织为Response格式发送给客户端
"""

from socket import *
import sys
import re
from config import *
from threading import Thread


# 服务器地址
ADDR = (HOST, PORT)


# 将httpserver的基础功能封装为类
class HTTPServer:
	def __init__(self):
		self.sockfd = None
		self.ip = None
		self.port = None
		self.addr = ADDR
		self.create_sock()
		self.bind()

	# 创建套接字
	def create_sock(self):
		self.sockfd = socket(AF_INET, SOCK_STREAM)
		self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

	# 绑定地址
	def bind(self):
		self.sockfd.bind(self.addr)
		self.ip = self.addr[0]
		self.port = self.addr[1]

	# 启动服务
	def serve_forever(self):
		self.sockfd.listen(5)
		print("Listen the port %d" % self.port)
		while True:
			connfd, addr = self.sockfd.accept()
			print("Connect from ", addr)
			client = Thread(target=self.handle, args=(connfd,))
			client.setDaemon(True)
			client.start()
			client.join()

	# 具体处理客户端请求任务
	def handle(self, connfd):
		# 获取HTTP请求
		request = connfd.recv(4096).decode()
		pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\w*?)\s+HTTP/1.1"
		try:
			env = re.match(pattern, request)
		except:
			# 客户端断开
			connfd.close()
			return
		else:
			print(env.groupdict())


httpd = HTTPServer()
httpd.serve_forever()


