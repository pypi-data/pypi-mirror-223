# -*- encoding: utf-8 -*-
"""
@File    :   strCheck.py
@Time    :   2023-03-02 23:52
@Author  :   坐公交也用券
@Version :   1.0
@Contact :   liumou.site@qq.com
@Homepage : https://liumou.site
@Desc    :   字符串检查
"""
import re


def CheckSqlInjection(text):
	"""
	检查输入文本是否包含SQL注入的敏感字符。
	返回True表示检测到了SQL注入敏感字符，否则返回False。
	"""
	sql_pattern = re.compile(
		r"(\b(ALTER|CREATE|DELETE|DROP|EXEC(UTE)?|INSERT( +INTO)?|MERGE( +INTO)?|SELECT|UPDATE)\b|\b(OR|AND|NOT) +\d)",
		re.IGNORECASE)
	if sql_pattern.search(text):
		return True
	return False


# 示例用法
if __name__ == "__main__":
	text = input("请输入文本：")
	if CheckSqlInjection(text):
		print("输入包含SQL注入敏感字符！")
	else:
		print("输入不包含SQL注入敏感字符。")
