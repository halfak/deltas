import re

from .tokenizer import Tokenizer

class TextSplit(Tokenizer):
	
	def tokenize(self, text):
		return re.findall(
			r"[\w]+|[,.?!]|[\n\ \t\r]+|.",
			text
		)
