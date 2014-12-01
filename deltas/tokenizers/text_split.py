import re

from .tokenizer import Tokenizer


class TextSplit(Tokenizer):
	"""
	Splits text into words, punctuation, whitespace and *everything else*.
	"""
	
	def tokenize(self, text):
		"""
		Tokenizes text.
		
		:Parameters:
			text : str
				Text to be tokenized
			
		:Returns:
			a `list` of `str` tokens
		"""
		return re.findall(
			r"[\w]+|[,.?!]|[\n\ \t\r]+|.",
			text
		)
	
	@classmethod
	def from_config(cls, doc, name):
		return cls()
