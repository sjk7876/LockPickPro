import bruteforce

def main():
    # password = "P@ssw0rd"
    password = "Change"
    algo = "md5"
    wordlist = "wordlists/fasttrack.txt"
    passwordHash = bruteforce.hashPasswordWithAlgo(password, algo)
    mangle = False
    
# Hashes
    # hash = input("Input hash to use: ")

# input pass + algo
    # password, algo = bruteforce.getPasswordFromStdIn()
    # passwordHash = bruteforce.hashPasswordWithAlgo(password, algo)

# input wordlist    
    # wordlist = "wordlists/" + input("Input the filename of the word list to use: ")
    
    print(bruteforce.crackPassword(passwordHash, wordlist, mangle))
            


if (__name__ == "__main__"):
    main()
