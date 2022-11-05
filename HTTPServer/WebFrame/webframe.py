"""
webframe.py WebFrame服务端
WebFrame功能：
  从httpserver接收具体请求
  根据请求进行逻辑处理和数据处理
  将需要的数据反馈给httpserver
"""

from socket import *
import json
from settings import *
from select import select


# 应用类，处理某一方面的请求
class Application:
	def __init__(self):
		self.sockfd = socket(AF_INET, SOCK_STREAM)
		self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
		self.sockfd.bind((frame_ip, frame_port))

	# 启动服务
	def start(self):
		self.sockfd.listen(5)
		print('Start app listen %s' % frame_port)
		c, addr = self.sockfd.accept()
		while True:
			data = c.recv(1024).decode()
			print(json.loads(data))
			d = {'status': '200', 'data': 'xxxxxx'}
			c.send(json.dumps(d).encode())


app = Application()
app.start()  # 启动应用服务

