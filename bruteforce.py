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


def getPasswordFromStdIn():
    password = input("Enter password to hash: ")
    algo = input("Enter algorithm to use (MD5, SHA1, SHA256): ").lower()
    
    while algo not in ("sha256", "sha1", "md5"):
        algo = input("Incorrect algorithm entered, please try again: ").lower()
        
    return password, algo


def hashPassword(password, algo):
    match algo:
        case "md5":
            return hashlib.md5(password.encode()).hexdigest()
        case "sha1":
            return hashlib.sha1(password.encode()).hexdigest()
        case "sha256":
            return hashlib.sha256(password.encode()).hexdigest()


def crackPassword(password):


def main():
    print()


if (__name__ == "__main__"):
    main()
