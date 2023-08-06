# -*- encoding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
	long_description = fh.read()
setuptools.setup(
	name="pbm",
	version="1.0.0",
	author="坐公交也用券",
	author_email="liumou.site@qq.com",
	description="主要用于字符串、数据对比、数据校验、数据清洗、敏感字符去除的模块",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://gitee.com/liumou_site/pbmd",
	packages=["pbm"],
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",

	],
	# Py版本要求
	python_requires='>=3.0',
	# 依赖
	install_requires=[]
)
