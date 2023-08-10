"""
This program finds a match for a hashed password via brute force.
Uses multi-threading to speed up process

@Author Spencer Kurtz
"""

import hashlib

"""
password sha1 	- 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
password sha256 - 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
password md5 	- 5f4dcc3b5aa765d61d8327deb882cf99
P@ssw0rd sha1	- 21bd12dc183f740ee76f27b78eb39c8ad972a757
P@ssword sha256 - b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342
P@ssword md5	- 161ebd7d45089b3446ee4e0d86dbcf92
"""

"""
TODO -
viewmodel -
	sha1 hashing
	sha256 hashing
	md5 hashing

	import password list

	have list of password wordlists that one can use
		provide user ability to select wordlist
	mangle option

	"generating word list"
	then go to progress bar after

	hash finding

	gpu threading

	potentially bcrypt
	potentially cpu multi threading

	option to input a plain-text password + hashing algo

cli -
	extremely basic
	"dank memes"

gui -
	loading bar
	select # cores
	etc
	"dank memes"

SEND TO EXE
"""


"""
Prompts user for a password and hashing algorithm to use

@return	String String, password to hash and algorithm to use
"""
def getPasswordFromStdIn():
	password = input("Enter password to hash: ")
	algo = input("Enter algorithm to use (MD5, SHA1, SHA256): ").lower()

	while algo not in ("sha256", "sha1", "md5"):
		algo = input("Incorrect algorithm entered, please try again: ").lower()

	return password, algo


"""
Hashes a given password based on the given algorithm

@param password		String, password to be hashed
@param algo			String, algorithm to use
@return				String, hex of hash
"""
def hashPasswordWithAlgo(password, algo):
	match algo:
		case "md5":
			return hashlib.md5(password.encode()).hexdigest()
		case "sha1":
			return hashlib.sha1(password.encode()).hexdigest()
		case "sha256":
	  		return hashlib.sha256(password.encode()).hexdigest()

"""
Given a password, returns a list of hashes

@param password		String, password to hash
@return				List, list of hash strings in hex
"""
def hashPasswordWithoutAlgo(password):
	return [hashlib.md5(password.encode()).hexdigest(),
			hashlib.sha1(password.encode()).hexdigest(),
			hashlib.sha256(password.encode()).hexdigest()]


"""
Given a hash, guesses the algorithm

@param password		String, hash to guess
@return				String, guessed algorithm
"""
def determineHashAlgo(password):
	if len(password) == 32:
		return "md5"
	elif len(password) == 40:
		return "sha1"
	elif len(password) == 64:
		return "sha256"

"""
Brute forces a given hash with a wordlist
If given the mangle flag, it calls a function to 'mangle' the list

@param hash		String, hash to find
@param file		String, word list to use
@param mangle	Bool, 
@return			password the hash is associated with or None
"""
def crackPassword(hash, file, mangle):
	try:
		with open(file, "r") as wordListFile:
			wordList = wordListFile.read().splitlines()
		
		if mangle:
			wordList = mangleList(wordList)

		for word in wordList:
			if hash in hashPasswordWithoutAlgo(word):
				return word
	except Exception:
		print("File does not exist")


def mangleList(wordList):
	return wordList


def main():
	print()


if (__name__ == "__main__"):
	main()
