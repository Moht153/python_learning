"""
数据库操作模块

思路：
建立一个数据库操作 类， 将dict_server 需要的数据库操作功能分别
协成方法，在dict_server中实例化对象，需要什么方法直接调用
"""
import pymysql
import hashlib

SALT = "#&Aid_"  # 设置加密时用的盐


class DBOperation:
	"""
	数据库操作类
	"""

	def __init__(self,
				 port=3306,
				 host="localhost",
				 user="root",
				 password="123456",
				 database="dict",
				 charset="utf8"):
		self.host = host
		self.user = user
		self.password = password
		self.database = database
		self.port = port
		self.charset = charset
		# 连接数据库
		self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
								  port=self.port,
								  charset=self.charset)

	# 建立游标
	def create_cursor(self):
		self.cur = self.db.cursor()

	# 关闭游标
	def cur_close(self):
		self.cur.close()

	# 关闭数据库连接
	def close(self):
		self.db.close()

	def query(self, data):
		sql = "select mean from words where word = %s;"
		self.cur.execute(sql, data)
		response = self.cur.fetchone()
		if response:
			return response[0]
		else:
			return

	def register(self, name, passwd):
		"""
		连接数据库，完成用户注册
		:param name: 注册姓名
		:param passwd: 注册密码
		:return: Bool 表示是否成功
		"""
		sql = "select name from user where name = '%s';" % name
		self.cur.execute(sql)
		# 查找到则表示用户已经存在，返回失败
		if self.cur.fetchone():
			return False
		passwd = self.hash_handle(name, passwd)

		sql = "insert into user (name, passwd) values (%s,%s)"
		try:
			self.cur.execute(sql, (name, passwd))
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			return False

	def insert_history(self, name, word):
		sql = "insert into history (name,word) values (%s,%s)"
		try:
			self.cur.execute(sql, (name, word))
			self.db.commit()
		except Exception:
			self.db.rollback()

	def do_hist(self, name):
		sql = "select name,word,time from history where name = %s" \
			  "order by time desc " \
			  "limit 10;"
		self.cur.execute(sql,(name,))
		re = self.cur.fetchall()
		re_list = []
		for item in re:
			info = "name: %s\tword: %s\ttime: %s" % (item[0], item[1], item[2])
			re_list.append(info)
		re = "\n".join(re_list)
		return re

	@staticmethod
	def hash_handle(name, passwd):
		hash = hashlib.md5((name + SALT).encode())  # 加盐处理
		hash.update(passwd.encode())  # 算法加密
		passwd = hash.hexdigest()  # 生成加密后的密码
		return passwd

	def login(self, name, passwd):
		"""
		连接数据库，完成用户登陆
		:param name: 用户传入的用户名
		:param passwd: 用户传入的密码
		:return: Bool 表示是否成功
		"""
		sql = "select passwd from user where name = '%s';" % name
		self.cur.execute(sql)
		result = self.cur.fetchone()
		print(result)
		# 对密码passwd进行加密存储处理
		passwd = self.hash_handle(name, passwd)
		# 没有查询到数据，则表示登陆用户不存在，无法登陆，返回1
		if not result:
			return 1
		# 有数据且密码匹配，表示登陆成功，返回2
		if result[0] == passwd:
			return 2
		# 有数据但密码不匹配，说明密码输入错误
		else:
			return 3
