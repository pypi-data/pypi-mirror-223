# -*- encoding: utf-8 -*-
"""
@File    :   strCheck.py
@Time    :   2023-03-02 23:52
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   字符串处理
"""


def RemoveSpecialSql(txt):
	"""
	移除Sql敏感字符
	:param txt: 需要处理的语句
	:return:
	"""
	pass


def FilterStr(data):
	"""
	过滤字符串
	:param data: 字符串
	:return:
	"""
	d = str(data).replace(" ", '').replace("\t", '').replace("\n", '').replace("-", '')
	d = str(d).replace("|", '').replace("\\", '').replace("/", '').replace("&", '')
	# d = str(d).replace("|", '').replace("\\", '').replace("/", '').replace("&", '')
	d = str(d).replace(">", '').replace("<", '').replace("select", '').replace("SELECT", '')
	return d
