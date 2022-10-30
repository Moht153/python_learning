"""
	程序入口
	为什么需要一个main文件：
	因为第一个运行的文件，不会被编译
	因此需要将入口文件单独拿出来，让程序其他部分被系统编译
"""
from ui import *

if __name__ == "__main__":
	sys01 = StudentManagerView()
	sys01.main()

