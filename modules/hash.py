
import hashlib

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