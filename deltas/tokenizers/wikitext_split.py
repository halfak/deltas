import re

from .tokenizer import Tokenizer


class WikitextSplit(Tokenizer):
	"""
	A tokenizer for splitting MediaWiki markup from other content.
	"""
	
	def tokenize(self, text):
		return re.findall(
			r"[\w]+|[.?!]+|[\n\ \t\r]+|\[\[|\]\]|\{\{|\}\}|&\w+;|'''|''|=+|\{\||\|\}|\|\-|.",
			text
		)
	
	@classmethod
	def from_config(cls, doc, name):
		return cls()
