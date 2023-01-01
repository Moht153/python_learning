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
from urls import *


# 应用类，处理某一方面的请求
class Application:
	def __init__(self):
		self.dir = settings_dir
		self.rlist = []
		self.wlist = []
		self.xlist = []
		self.sockfd = socket(AF_INET, SOCK_STREAM)
		self.sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, DEBUG)
		self.sockfd.bind((frame_ip, frame_port))

	# 启动服务
	def start(self):
		self.sockfd.listen(5)
		print('Start app listen %s' % frame_port)
		self.rlist.append(self.sockfd)
		# select 监控请求
		while True:
			rs, ws, xs = select(self.rlist, self.wlist, self.xlist)

			for r in rs:
				if r is self.sockfd:
					connfd, addr = r.accept()
					self.rlist.append(connfd)
				else:
					self.handle(r)
					self.rlist.remove(r)


	def handle(self, connfd):
		data = connfd.recv(1024).decode()
		data = json.loads(data)
		# data => {'method': 'GET', 'info': '/'}
		if data['method'] == 'GET':
			if data['info'] == '/' or data['info'][-5:] == '.html':
				response = self.get_html(data['info'])
			else:
				response = self.get_data(data['info'])

		elif data['method'] == 'POST':
			pass
		# 将数据发送给httpserver
		# response = {'status': '200', 'data': 'xxxxx'}
		response = json.dumps(response)
		connfd.send(response.encode())
		connfd.close()

	# 处理网页
	def get_html(self, filename):
		if filename == '/':
			# 请求主页
			filename = self.dir + '/index.html'
		else:
			filename = self.dir + filename
		response_html = {'status': '', 'data': ''}
		try:
			file = open(filename, 'r')
		except Exception:
			# 网页不存在
			filename = self.dir + '/404.html'
			file = open(filename, 'r')

			response_html['status'] = '404'
			response_html['data'] = file.read()
			file.close()
			return response_html
		else:
			# 网页存在
			response_html['status'] = '200'
			response_html['data'] = file.read()
			file.close()
			return response_html

	# 处理数据
	def get_data(self, info):
		for url,func in urls:
			if url == info:
				return {'status': '200', 'data': func()}
		return {'status': '200', 'data': "Sorry..."}


app = Application()
app.start()  # 启动应用服务

