import getpass  # 隐藏输入
import hashlib  # 转换加密

# 输入隐藏
pwd = getpass.getpass("PW:")
print(pwd)

# # hash对象
# hash = hashlib.md5(())  # 生成md5 加密对象

# 算法加盐(#$awv3_) 一般来说，就是在用户输入的密码中的特定位置加入制定的特殊字符，产生迷惑性
hash = hashlib.md5("Moht%%……".encode())  # 生成md5并制定特殊字符串对密码自动加盐
hash.update(pwd.encode())  # 算法加密
pwd = hash.hexdigest()  # 提取加密后的密码

print(pwd)