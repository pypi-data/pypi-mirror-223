# -*- encoding: utf-8 -*-
"""
@File    :   listHandle.py
@Time    :   2023-03-03 00:05
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   列表处理
"""


def ListRemoveNone(lists=[]):
	"""
	列表移除空元素、空格元素
	:param lists: 需要移除的列表
	:return:
	"""
	for i in lists:
		if i is None or str(i) == '' or str(i) == " ":
			lists.remove(i)
	return lists


def ListToStr(lists=[], sep=""):
	"""
	列表元素转换成字符串
	:param lists: 需要转换的列表
	:param sep: 元素之间的拼接符(默认: 无)
	:return:
	"""
	txt = ""
	for i in lists:
		txt = str(txt) + str(i) + str(sep)
	return txt
