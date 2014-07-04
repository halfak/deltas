
from collections import namedtuple

Operation = namedtuple("Operation", ['name', 'a1', 'a2', 'b1', 'b2'])

""" This operation is useless and will be ignored
class Replace(Operation):
	def __init__(self, a1, a2, b1, b2):
		Operation.__init__(self, "replace", a1, a2, b1, b2)
"""

class Delete(Operation):
	def __new__(cls, a1, a2, b1, b2):
		return Operation.__new__(cls, "delete", a1, a2, b1, b2)

class Insert(Operation):
	def __new__(cls, a1, a2, b1, b2):
		return Operation.__new__(cls, "insert", a1, a2, b1, b2)

class Equal(Operation):
	def __new__(cls, a1, a2, b1, b2):
		return Operation.__new__(cls, "equal", a1, a2, b1, b2)
