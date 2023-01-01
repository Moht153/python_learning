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


# 和web frame 通信的函数
def connect_frame(env):
	frame_addr = (frame_ip, frame_port)
	s = socket(AF_INET, SOCK_STREAM)
	try:
		s.connect(frame_addr)
	except Exception as e:
		print(e)
		sys.exit()
	else:
		# 将字典转换为json
		data = json.dumps(env)
		# 将解析后的请求发送给webframe
		print("send to webframe", data)
		s.send(data.encode())
		# 接收来自webframe数据
		data = s.recv(4096 * 100).decode()
		# print(json.loads(data))
		return json.loads(data)


# 将httpserver的基础功能封装为类
class HTTPServer:
	def __init__(self):
		self.sockfd = None
		self.connect_sockfd = None
		self.ip = None
		self.port = None
		self.addr = ADDR
		self.create_socket()  # 和浏览器交互
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
		pattern = r"(?P<method>[A-Z]+)\s+(?P<info>/\w*\.?\w*)\s+HTTP/1.1"
		try:
			env = re.match(pattern, request).groupdict()
			print(env)
		except:
			# 客户端断开
			print('re有问题')
			connfd.close()
			return
		else:
			data = connect_frame(env)
			# 防止一端突然断开，返回None
			print(data)
			if data:
				self.response(connfd, data)

	# 给浏览器发送数据
	@staticmethod
	def response(connfd, data):
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


