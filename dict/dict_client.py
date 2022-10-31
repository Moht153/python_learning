"""
dict 客户端

功能：根据用户输入，发送请求，得到结果
结构： 一级界面 --> 注册、登陆、退出
	  二级界面 --> 查单词、 历史记录、 注销
"""


import socket
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
		==================Welcome=====================
		1. 注册			   2. 登陆                3.退出
		""")
		cmd = input("输入选项：")
		if cmd == "1":
			do_register()
		elif cmd == "2":
			s.send(cmd.encode())
		elif cmd == "3":
			s.send(cmd.encode())
		else:
			print("请输入正确选项")



def do_register():
	while True:
		name = input("请输入姓名(不允许有空格)：")
		passwd = input("请输入密码(不允许有空格)：")
		passwd1 = input("再次输入密码确认(不允许有空格)：")
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
		return True
	else:
		print("注册失败，请重新注册")
		return False


if __name__ == "__main__":
	main()
