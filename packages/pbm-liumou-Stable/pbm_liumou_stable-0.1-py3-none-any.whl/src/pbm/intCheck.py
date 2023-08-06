# -*- encoding: utf-8 -*-
"""
@File    :   intCheck.py
@Time    :   2023-03-02 23:52
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   整数处理
"""


class IntCheck:
	def __init__(self):
		self.Err = None
	
	def CheckValue(self, start, stop, total):
		"""
		检查传入的数值是否符合实际要求
		:param total: 总数
		:param start: 开始数
		:param stop: 截止数
		:return: bool
		"""
		self.Err = None
		if int(start) >= int(stop):
			self.Err = "开始数大于截止数"
			return False
		if int(stop) > int(total):
			self.Err = "截止数大于实际数"
			return False
		if int(total) <= int(start):
			self.Err = "实际数小于开始数"
			return False
		return True
