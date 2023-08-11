import bruteforce

def main():
    # password = "P@ssw0rd"
    password = "password"
    algo = "md5"
    wordlist = "wordlists/fasttrack.txt"
    passwordHash = bruteforce.hashPasswordWithAlgo(password, algo)
    mangle = False

    algo = bruteforce.determineHashAlgo(passwordHash)
    
# Hashes
    # hash = input("Input hash to use: ")

# input pass + algo
    # password, algo = bruteforce.getPasswordFromStdIn()
    # passwordHash = bruteforce.hashPasswordWithAlgo(password, algo)

# input wordlist    
    # wordlist = "wordlists/" + input("Input the filename of the word list to use: ")

    # print(bruteforce.startCrack(passwordHash, algo, wordlist, mangle))

    # print("cuda", bruteforce.get_cuda_cores())
    bruteforce.startCrackWithCPU(passwordHash, algo, wordlist, mangle)
            


if (__name__ == "__main__"):
    main()
