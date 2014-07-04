import re

from .tokenizer import Tokenizer

class WikitextSplit(Tokenizer):
	
	def tokenize(self, text):
		return re.findall(
			r"[\w]+|[.?!]+|[\n\ \t\r]+|\[\[|\]\]|\{\{|\}\}|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
			text
		)
