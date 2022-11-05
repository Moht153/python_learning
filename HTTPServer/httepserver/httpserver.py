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
import json


# 服务器地址
ADDR = (HOST, PORT)


# 将httpserver的基础功能封装为类
class HTTPServer:
	def __init__(self):
		self.sockfd = None
		self.connect_sockfd = None
		self.ip = None
		self.port = None
		self.addr = ADDR
		self.create_socket()  # 和浏览器交互
		self.connect_socket()  # 和WebFrame交互
		self.bind()

	# 创建套接字
	def create_socket(self):
		self.sockfd = socket(AF_INET, SOCK_STREAM)
		self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)

	# 绑定地址
	def bind(self):
		self.sockfd.bind(self.addr)
		self.ip = self.addr[0]
		self.port = self.addr[1]

	# 创建WebFrame交互套接字
	def connect_socket(self):
		self.connect_sockfd = socket(AF_INET, SOCK_STREAM)
		frame_addr = (frame_ip, frame_port)
		try:
			self.connect_sockfd.connect(frame_addr)
		except Exception as e:
			print(e)
			sys.exit()

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
			env = re.match(pattern, request).groupdict()
			print(env)
		except:
			# 客户端断开
			connfd.close()
			return
		else:
			# 将字典转换为json
			data = json.dumps(env)
			# 将解析后的请求发送给webframe
			print("send", data)
			self.connect_sockfd.send(data.encode())
			# 接收来自webframe数据
			data = self.connect_sockfd.recv(4096).decode()
			print(json.loads(data))
			self.response(connfd, json.loads(data))
			return

	# 给浏览器发送数据
	def response(self, connfd, data):
		# data => {'status': '200', 'data': 'xxxxxx'}
		if data['status'] == '200':
			response_headers = "HTTP/1.1 200 OK\r\n"
			response_headers += "Content-Type:Text/html\r\n"
			response_headers += "\r\n"
			response_body = data['data']
			
		elif data['status'] == '404':
			response_headers = "HTTP/1.1 404 OK\r\n"
			response_headers += "Content-Type:Text/html\r\n"
			response_headers += "\r\n"
			response_body = data['data']

		elif data['status'] == '500':
			pass

		# 给浏览器发送数据
		response_data = response_headers + response_body
		connfd.send(response_data.encode())

httpd = HTTPServer()
httpd.serve_forever()


