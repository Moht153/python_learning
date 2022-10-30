"""
	装饰器
"""
# 需求：对一下两个功能增加权限验证。

"""
def verify_permission():
	print("权限验证")


# 已有功能
def enter_background():
	verify_permission()
	print("进入后台")


def delete_order():
	verify_permission()
	print("删除订单")


"""

# 以上函数存在缺点，增加功能，需要修改已有功能。（违反开闭原则）

"""
# 需要增加的功能
def verify_permission(func):
	def wrapper():
		print("权限验证")
		func()

	return wrapper


# 已有功能
def enter_background():
	print("进入后台")


def delete_order():
	print("删除订单")


enter_background = verify_permission(enter_background)
delete_order = verify_permission(delete_order)
enter_background()
delete_order()
# 存在缺点，每次对已有功能拦截enter_background/delete_order 不科学。"""

"""
缺点：
必须要在
enter_background = verify_permission(enter_background)
delete_order = verify_permission(delete_order)
之后调用才能拦截
"""


def verify_permission(func):
	def wrapper(*args, **kwargs):
		print(args)
		print(kwargs)
		print("权限验证")
		func(*args, **kwargs)

	return wrapper


# 已有功能
@verify_permission
def enter_background(login_id,pwd):
	# enter_background = verify_permission(enter_background)
	print("%s login in..."%login_id)
	print("Your password is %s"% pwd)
	print("进入后台")


@verify_permission
def delete_order(order_id):
	# delete_order = verify_permission(delete_order)
	print("%d号订单已删除" % order_id)


enter_background(1142, pwd='mht')
delete_order(93)
