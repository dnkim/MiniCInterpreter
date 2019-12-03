class Result:
	def __init__(self, value = None):
		self.value = value

class Ok(Result):
	pass

class Err(Result):
	pass
