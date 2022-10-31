"""
数据库操作模块

思路：
建立一个数据库操作 类， 将dict_server 需要的数据库操作功能分别
协成方法，在dict_server中实例化对象，需要什么方法直接调用
"""
import pymysql


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

	# def connect_database(self):
	# 	self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database,
	# 							  port=self.port,
	# 							  charset=self.charset)

	# 建立游标
	def create_cursor(self):
		self.cur = self.db.cursor()

	# 关闭游标
	def cur_close(self):
		self.cur.close()

	# 关闭数据库连接
	def close(self):
		self.db.close()

	def handle(self, data):
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
		# 如果已经存在，返回失败
		if self.cur.fetchone():
			return False
		sql = "insert into user (name, passwd) values (%s,%s)"
		try:
			self.cur.execute(sql, (name, passwd))
			self.db.commit()
			return True
		except Exception as e:
			self.db.rollback()
			return False


