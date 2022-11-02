"""
dict 客户端

功能：根据用户输入，发送请求，得到结果
结构： 一级界面 --> 注册、登陆、退出
	  二级界面 --> 查单词、 历史记录、 注销
"""


import socket
import sys
from getpass import getpass  # 运行使用终端

# 服务器地址
HOST = '127.0.0.1'
PORT = 9527
ADDR = (HOST, PORT)
# 创建TCP流式套接字
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(ADDR)


# 搭建客户端网络
def main():
	while True:
		print("""
		=========================Welcome=========================
		1. 注册			   2. 登陆                3.退出
		""")
		cmd = input("输入选项：")
		if cmd == "1":
			do_register()
		elif cmd == "2":
			is_next = do_login()
			if is_next[0]:
				# 如果 do_login()返回True,进入二级子界面
				second_ui(is_next[1])
			else:
				if input("是否注册？ y --yes; n -- no") == 'y':
					do_register()
				else:
					continue
		elif cmd == "3":
			do_quit()
			return
		else:
			print("请输入正确选项")


def second_ui(name):
	while True:
		print("""
		=========================Query=========================
		1. 单词查询		2. 查看历史记录         3. 注销
		""")
		cmd = input("请输入指令：")
		if cmd == "1":
			do_query(name)
		elif cmd == "2":
			do_hist(name)
		elif cmd == "3":
			print("返回登录界面……")
			break



def do_register():
	while True:
		name = input("===================用户注册===================\n"
					 "请输入姓名(不允许有空格)：")
		passwd = getpass("请输入密码(不允许有空格)：")
		passwd1 = getpass("再次输入密码确认(不允许有空格)：")
		if passwd != passwd1:
			print("两次密码输入不一致，请重新输入～")
			continue
		if " " in name or " " in passwd:
			print("姓名和密码不允许有空格")
			continue
		break
	message = 'R %s %s' % (name, passwd)
	s.send(message.encode())  # 发送给服务端
	answer = s.recv(32).decode()  # 接收服务端结果
	if answer == "OK":
		print("注册成功")
		second_ui(name)
	else:
		print("注册失败，请重新注册")


def do_login():
	while True:
		name = input("请输入姓名(不允许有空格，不输入退出)：")
		passwd = getpass("请输入密码(不允许有空格)：")
		# 这里做了一个退出的选择
		if not name:
			return False, None
		message = "L %s %s" % (name, passwd)
		s.send(message.encode())  # 发送给服务端
		answer = s.recv(32).decode()  # 接收服务端结果
		if answer == "OK":
			print("登陆成功")
			return True, name
		elif answer == "NU":
			print("用户不存在，请注册～")
			return False, name
		else:
			print("登陆失败，用户名或密码输入有误～")
			continue


def do_query(name):
	"""
	执行单词查找功能
	name: 因为查询要记录历史记录，因此还要向服务端上传用户名
	:return: None
	"""
	while True:
		word = input("请输入要查询的单词(输入空退出)：")
		if not word:
			break
		message = "Q %s %s" % (word, name)
		s.send(message.encode())  # 发送信息给服务端
		answer = s.recv(1024).decode()  # 接收服务端查询结果
		print(answer)
	print("返回上级菜单...")


def do_hist(name):
	"""
	执行查看历史记录功能
	查看最近查找的10条记录
	:return: None
	"""
	message = "H %s" % name
	s.send(message.encode())  # 发送信息给服务端
	while True:
		answer = s.recv(128).decode()  # 接收服务端查询结果
		if answer == "##":
			break
		print(answer)
	print("返回上级菜单...")


def do_quit():
	"""
	退出操作，向服务端发出退出请求，断开连接
	:return: None
	"""
	message = "E".encode()
	s.send(message)
	sys.exit("谢谢使用～")

if __name__ == "__main__":
	main()
