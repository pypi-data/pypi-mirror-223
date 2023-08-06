"""
	#################################
	# STACK IMPLEMENTATION [PYTHON] #
	#################################
	
	NOTES 
		* array based 
		* does not require other files
		* printable / narrow width

	API 
		Stack 
			- size()
			- top() 
			- push(value) 
			- pop()
			- is_empty()
			- clear()

"""

class Stack: 
	def __init__(self): 
		self.items = [] 

	def size(self):
		return len(self.items) 
	
	def top(self): 
		return self.items[-1] 
	
	def push(self, value): 
		self.items.append(value)
	
	def pop(self): 
		return self.items.pop(self.size() - 1) 

	def is_empty(self): 
		return self.size() == 0 
		 
	def clear(self): 
		self.items = []