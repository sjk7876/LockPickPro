import bruteforce

def main():
    password, algo = bruteforce.getPasswordFromStdIn()
    
    print(bruteforce.hashPassword(password, algo))
            
    # masterHash = input("Input hash to use: ")


if (__name__ == "__main__"):
    main()
