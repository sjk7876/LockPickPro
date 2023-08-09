"""
This program finds a match for a hashed password via brute force.
Uses multi-threading to speed up process

@Author Spencer Kurtz
"""

"""
password sha1 	- 
password sha256 - 
password md5 	- 
P@ssw0rd sha1	- 
P@ssword sha256 - 
P@ssword md5	- 
"""

"""
TODO - 
viewmodel - 
	sha1 hashing
	sha256 hashing
	md5 hashing
 
	import password list
	random password generation
 
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
"""


def getPasswordFromStdIn():
    password = input("Enter password to hash: ")
    algo = input("Enter algorithm to use (MD5, SHA1, SHA256): ").lower()
    
    while algo not in ("SHA256", "sha1", "md5"):
        algo = input("Incorrect algorithm entered, please try again: ").lower()
        
    return password, algo


def main():
    password, algo = getPasswordFromStdIn()
    print(password, algo)


if (__name__ == "__main__"):
    main()
