"""
This program finds a match for a hashed password via brute force.
Uses multi-threading to speed up process

@Author Spencer Kurtz
"""

import hashlib

from itertools import product

# GPU Acceleration
import numpy
# import numba
# from numba import cuda

# CPU Multi-threading
import threading
import multiprocessing

import time

"""
password sha1 	- 5baa61e4c9b93f3f0682250b6cf8331b7ee68fd8
password sha256 - 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
password md5 	- 5f4dcc3b5aa765d61d8327deb882cf99
P@ssw0rd sha1	- 21bd12dc183f740ee76f27b78eb39c8ad972a757
P@ssword sha256 - b03ddf3ca2e714a6548e7495e2a03f5e824eaac9837cd7f159c67b90fb4b7342
P@ssword md5	- 161ebd7d45089b3446ee4e0d86dbcf92
"""


"""
TODO
Move mangling to inside threading
do one mangle at a time
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
@cuda.jit
def get_cuda_cores():
    ""
    Retrieve the number of CUDA cores in the GPU.
    ""
    device = cuda.get_current_device()
    cuda_cores = device.MULTIPROCESSOR_COUNT * device.WARP_SIZE
    return cuda_cores
"""
"""
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
"""
"""
def startCrackWithGPU(passwordHash, algo, file, mangle):
	""
	Brute forces a given hash with a wordlist with a GPU
	If given the mangle flag, it calls a function to 'mangle' the list

	@param hash		String, hash to find
	@param algo		String, algorithm used for hash
	@param file		String, word list to use
	@param mangle	Bool, 
	@return			password the hash is associated with or None
	""

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
	# crackPassword[blocksPerGrid, threadsPerBlock](d_wordList, passwordHash, algo, d_result)
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
"""


# Global variable to stop thread execution
cancelThreads = False

# Global variable to return solution
solution = None


def getPasswordFromStdIn():
	"""
	Prompts user for a password and hashing algorithm to use

	Returns:
		String, String: Password to hash, Algorithm to use
	"""

	password = input("Enter password to hash: ")
	algo = input("Enter algorithm to use (MD5, SHA1, SHA256): ").lower()

	while algo not in ("sha256", "sha1", "md5"):
		algo = input("Incorrect algorithm entered, please try again: ").lower()

	return password, algo


def hashPasswordWithAlgo(password, algo):
	"""
	Hashes a given password based on the given algorithm

	Args:
		password (String): Password to hash
		algo (String): Algorithm to use

	Returns:
		String: hex value of hash
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

	Args:
		password (String): Password to hash

	Returns:
		List: List of hash values in hex
	"""

	return [hashlib.md5(password.encode()).hexdigest(),
			hashlib.sha1(password.encode()).hexdigest(),
			hashlib.sha256(password.encode()).hexdigest()]


def determineHashAlgo(password):
	"""
	Given a hash, guesses the algorithm

	Args:
		password (String): Hash to guess

	Returns:
		String: Name of guessed algorithm
	"""

	if len(password) == 32:
		return "md5"
	elif len(password) == 40:
		return "sha1"
	elif len(password) == 64:
		return "sha256"


def crackPassword(passwordHash, algo, wordList, mangle):
	"""
	Attempts to find a hash value that matches the given hash using a word list
	If given the mangle flag, creates variants of each word with random chars, capitalization, etc

	Args:
		passwordHash (String): Hash to match
		algo (String): Hashing algorithm to test with
		wordList (List): List of words to use
		mangle (Bool): Mangles each words
	"""
	global cancelThreads
	global solution
	
	for word in wordList:
		mangledList = [word]

		if cancelThreads or type(word) is list:
			return

		if mangle and word != "":
			mangledList = mangleList(word)

		for mangle in mangledList:
			if algo == "md5" and hashlib.md5(mangle.encode()).hexdigest() == passwordHash:
				cancelThreads = True
				solution = mangle
				return
				
			if algo == "sha1" and hashlib.sha1(mangle.encode()).hexdigest() == passwordHash:
				cancelThreads = True
				solution = mangle
				return
			
			if algo == "sha256" and hashlib.sha256(mangle.encode()).hexdigest() == passwordHash:
				cancelThreads = True
				solution = mangle
				return

	
def startCrackWithCPU(passwordHash, algo, file, mangle):
	"""
	Brute forces a given hash with a wordlist with multi-threading
	If given the mangle flag, it calls a function to 'mangle' the list

	Args:
		passwordHash (String): Hash to match
		algo (String): Algorithm to use
		file (String): File containing word list
		mangle (Bool): Flag to mangle each word

	Returns
		String: Returns found word or None type
	"""
	tic = time.perf_counter()
	try:
		with open(file, "r") as wordListFile:
			wordList = wordListFile.read().splitlines()
	except Exception:
		print(Exception)
		print("Error reading file")
		return None

	# w/ multiprocessing
	numThreads = 12
	seperatedList = list(divideList(wordList, numThreads))

	# Create threads
	threads = []
	for i in range(numThreads):
		thread = multiprocessing.Process(target=crackPassword, args=(passwordHash, algo, seperatedList[i], mangle))
		threads.append(thread)
		thread.start()

	for thread in threads:
		thread.join()

	# w/ threading
	# numThreads = 8
	# seperatedList = list(divideList(wordList, numThreads))

	# # Create threads
	# threads = []
	# for i in range(numThreads):
	# 	thread = threading.Thread(target=crackPassword, args=(passwordHash, algo, seperatedList[i], True))
	# 	threads.append(thread)
	# 	thread.start()

	# for thread in threads:
	# 	thread.join()

	# crackPassword(passwordHash, algo, seperatedList, mangle)

	result = solution if solution is not None else None

	if result is not None:
		print("Password found:", result)
	elif mangle:
		print("Password not in given word list nor is a variation of a word in the word list")
	else:
		print("Password not found in the given word list.")
	
	toc = time.perf_counter()
	print(f"{toc - tic:0.4f} seconds")

	return result


def divideList(list, num):
	"""
	Divides a list into num sublists

	Args:
		list (List): List to subdivide
		num (Int): Number of chunks

	Yields:
		List: List containing subdivided list, each of size Size
	"""

	for i in range(num):
		yield list[i::num]


def mangleList(masterWord):
	"""
	Given a word, generates a list of variants that are 'mangled'

	Args:
		masterWord (String): Word to mangle

	Returns:
		List: String list of mangled words
	"""
	# do mangle shit
	"""
	lowercase
	uppercase
	numbers
	symbols
	common add ons (123)
	leet
	"""
	wordList = [masterWord, masterWord.upper()]
	wordList.append(masterWord.lower())

	temp = masterWord[0].upper()
	for i in range(1, len(masterWord)):
		temp += masterWord[i]

	wordList.append(temp)

	wordListRecurse = []
	[wordListRecurse.append(x) for x in wordList if x not in wordListRecurse]

	for _ in range(2):
		temp = []
		for x in wordListRecurse:
			temp.extend(generateLeetVariants(x))
			temp.extend(generateSymbolVariants(x))
		wordListRecurse.extend(temp)
	
	temp = []
	for x in wordListRecurse:
		temp.extend((f"{x}1", f"{x}123", f"{x}abc", f"{x}!")) # Append common patterns
		temp.extend((f"1{x}", f"123{x}", f"abc{x}", f"!{x}")) # Prepend common patterns

		for i in range(1970, 2023):
			temp.append(x + str(i))
			temp.append(str(i) + x)

	wordListRecurse.extend(temp)
	
	res = []
	[res.append(x) for x in wordListRecurse if x not in res]

	return res


def generateLeetVariants(word):
	"""
	Generates leet variants of a word

	Args:
		word (String): original word

	Returns:
		List: String list of word variants
	"""

	replace = {'a': '4', 'b': '8', 'e': '3', 'g': '6', 'i': '1', 'o': '0', 's': '5', 't': '7', 'z': '2'}

	possibles = []
	for l in word:
		ll = replace.get(l, l)
		possibles.append( (l,) if ll == l else (l, ll) )
	
	return [ ''.join(t) for t in product(*possibles) ]


def generateSymbolVariants(word):
	"""
	Generates symbol variants of a word (ex pass can become pa$$)

	Args:
		word (String): original word

	Returns:
		List: String list of symbol variants
	"""

	replace = {'a': '@', 's': '$'}

	possibles = []
	for l in word:
		ll = replace.get(l, l)
		possibles.append( (l,) if ll == l else (l, ll) )
	
	return [ ''.join(t) for t in product(*possibles) ]


def main():
	print()


if (__name__ == "__main__"):
	main()
