
'''
Hash module for calculating hash of strings
'''

import hashlib

all_available_algs = ['md5','sha1','sha256','sha512']

def md5(word):
	
	hashtype = hashlib.md5()

	word = word.strip("\n")
	hashtype.update(word.encode('utf-8'))
	checkedHash = hashtype.hexdigest()

	return {'hash':checkedHash,'word':word}

def sha1(word):
	hashtype = hashlib.sha1()
	
	word = word.strip("\n")
	hashtype.update(word.encode('utf-8'))
	checkedHash = hashtype.hexdigest()

	return {'hash':checkedHash,'word':word}

def sha256(word):
	hashtype = hashlib.sha256()

	word = word.strip("\n")
	hashtype.update(word.encode('utf-8'))
	checkedHash = hashtype.hexdigest()

	return {'hash':checkedHash,'word':word}

def sha512(word):
	hashtype = hashlib.sha512()

	word = word.strip('\n')
	hashtype.update(word.encode('utf-8'))
	checkedhash = hashtype.hexdigest()

	return {'hash':checkedhash ,'word':word}

class HashManager:

	def __init__(self ,msg=None):
		self.msg = msg

	def calculate_hash(self):
		if self.msg:
			return self.check_alg()

	def check_alg(self):

		hashing_alg_and_string = self.msg.split(' ')
		if len(hashing_alg_and_string) >= 2:
			if hashing_alg_and_string[0] in all_available_algs:
				string = " ".join(hashing_alg_and_string[1:])
				alg = hashing_alg_and_string[0]

				if alg == 'md5':
					return md5(string)
				elif alg == 'sha1':
					return sha1(string)
				elif alg == 'sha256':
					return sha256(string)
				elif alg == 'sha512':
					return sha512(string)

		else:
			return None

	def show_help(self):
		temp_msg = "\n\t\t\t".join(all_available_algs)
		help_msg = '''
		```
z! hash algorithm your_string
z! hash md5 IAmTalas

	available algorithmes :
		    {}
		```
		'''
		help_msg = help_msg.format(temp_msg)
		return help_msg
