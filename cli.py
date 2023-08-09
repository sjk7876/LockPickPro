import bruteforce

def main():
    password = "P@ssw0rd"
    algo = "md5"
    wordlist = "wordlists/fasttrack.txt"
    # hash = bruteforce.hashPasswordWithAlgo(password, algo)
    
    hash = input("Input hash to use: ")

    
    # password, algo = bruteforce.getPasswordFromStdIn()
    
    # hash = bruteforce.hashPasswordWithAlgo(password, algo)

    # print(bruteforce.hashPasswordWithAlgo(password, algo))
    
    # wordlist = "wordlists/" + input("Input the filename of the word list to use: ")
    
    print(bruteforce.crackPassword(hash, wordlist))
            


if (__name__ == "__main__"):
    main()
