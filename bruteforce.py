"""
This program finds a match for a hashed password via brute force.
Uses multi-threading to speed up process

@Author Spencer Kurtz
"""

import hashlib

# GPU Acceleration
import numpy
import numba
from numba import cuda

# CPU Multi-threading
import threading

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


@cuda.jit
def get_cuda_cores():
    """
    Retrieve the number of CUDA cores in the GPU.
    """
    device = cuda.get_current_device()
    cuda_cores = device.MULTIPROCESSOR_COUNT * device.WARP_SIZE
    return cuda_cores


@cuda.jit
def crackPassword(wordList, passwordHash, algo, result):
	print("gg")
	i = cuda.grid(1)
	print("efg")

	if i < wordList.shape[0]:
		word = wordList[i]
		
		if algo == "md5" and hashlib.md5(word.encode()).hexdigest() == passwordHash: 
			result[0] = i
			result[1] = 1
		if algo == "sha1" and hashlib.sha1(word.encode()).hexdigest() == passwordHash:
			result[0] = i
			result[1] = 1
		if algo == "sha256" and hashlib.sha256(word.encode()).hexdigest() == passwordHash:
			result[0] = i
			result[1] = 1


def getPasswordFromStdIn():
	"""
	Prompts user for a password and hashing algorithm to use

	@return	String String, password to hash and algorithm to use
	"""

	password = input("Enter password to hash: ")
	algo = input("Enter algorithm to use (MD5, SHA1, SHA256): ").lower()

	while algo not in ("sha256", "sha1", "md5"):
		algo = input("Incorrect algorithm entered, please try again: ").lower()

	return password, algo


def hashPasswordWithAlgo(password, algo):
	"""
	Hashes a given password based on the given algorithm

	@param password		String, password to be hashed
	@param algo			String, algorithm to use
	@return				String, hex of hash
	"""

	if algo == "md5":
		return hashlib.md5(password.encode()).hexdigest()
	elif algo == "sha1":
		return hashlib.sha1(password.encode()).hexdigest()
	elif algo == "sha256":
		return hashlib.sha256(password.encode()).hexdigest()


def hashPasswordWithoutAlgo(password):
	"""
	Given a password, returns a list of hashes

	@param password		String, password to hash
	@return				List, list of hash strings in hex
	"""

	return [hashlib.md5(password.encode()).hexdigest(),
			hashlib.sha1(password.encode()).hexdigest(),
			hashlib.sha256(password.encode()).hexdigest()]


def determineHashAlgo(password):
	"""
	Given a hash, guesses the algorithm

	@param password		String, hash to guess
	@return				String, guessed algorithm
	"""

	if len(password) == 32:
		return "md5"
	elif len(password) == 40:
		return "sha1"
	elif len(password) == 64:
		return "sha256"


def startCrackWithGPU(passwordHash, algo, file, mangle):
	"""
	Brute forces a given hash with a wordlist with a GPU
	If given the mangle flag, it calls a function to 'mangle' the list

	@param hash		String, hash to find
	@param algo		String, algorithm used for hash
	@param file		String, word list to use
	@param mangle	Bool, 
	@return			password the hash is associated with or None
	"""

	# try:
	with open(file, "r") as wordListFile:
		wordList = wordListFile.read().splitlines()
	
	# if mangle:
	# 	wordList = mangleList(wordList)

	print("e")
	d_wordList = cuda.to_device(numpy.array(wordList))
	print("E")
	d_result = cuda.device_array((2,), dtype=numpy.int32)


	print("Eee")
	threadsPerBlock = 32
	blocksPerGrid = (len(wordList) + (threadsPerBlock - 1)) // threadsPerBlock

	print("EEEE")
	crackPassword[blocksPerGrid, threadsPerBlock](d_wordList, passwordHash, algo, d_result)
	print("ff")
	result = d_result.copy_to_host()
	print("FFF")
	if result[1] == 1:
		print("Password found:", wordList[result[0]])
	else:
		print("Password not found in the given word list.")

		# for word in wordList:
		# 	if passwordHash in hashPasswordWithAlgo(word, algo):
		# 		return word
	# except Exception:
	# 	print(Exception)
	# 	print("File does not exist")


def startCrackWithCPU(passwordHash, algo, file, mangle):
	"""
	Brute forces a given hash with a wordlist with multi-threading
	If given the mangle flag, it calls a function to 'mangle' the list
		
	@param hash		String, hash to find
	@param algo		String, algorithm used for hash
	@param file		String, word list to use
	@param mangle	Bool, 
	@return			password the hash is associated with or None
	"""
	
	# try:
	with open(file, "r") as wordListFile:
		wordList = wordListFile.read().splitlines()
	
	numThreads = 4

	seperatedList = divideList(wordList, numThreads)

	# if mangle:
	# 	wordList = mangleList(wordList)

	


	if result[1] == 1:
		print("Password found:", wordList[result[0]])
	else:
		print("Password not found in the given word list.")

		# for word in wordList:
		# 	if passwordHash in hashPasswordWithAlgo(word, algo):
		# 		return word
	# except Exception:
	# 	print(Exception)
	# 	print("File does not exist")


def divideList(list, size):
	"""
	Divides a list into chunks

	@param list		List, list to divide
	@param size		int, size of chunks
	@return			returns a list of lists
	"""

	for i in range(0, len(list), size):
		yield list[i:i + size]


def mangleList(wordList):
	return wordList


def main():
	# x = get_cuda_cores()
	# print(x)
	print(cuda.gpus)


if (__name__ == "__main__"):
	main()
