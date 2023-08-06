class Error:
	def __init__(self, msg: str, nil=True):
		"""
		异常处理
		:param msg: 异常信息(字符串)
		:param nil: 借鉴Go语言的Nil，该值是一个布尔值,判断是否存在错误
		"""
		self.Nil = nil
		self.Msg = msg

	def errors(self):
		"""
		返回错误信息
		:return: str
		"""
		return self.Msg
