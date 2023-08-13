# Secure Client Server Environment
## About
The given prompt for this project was to develop a Penetration Testing Tool.<br>
This project is an attempt at making something similar to John The Ripper, a brute-force application to find the password relating to a given hash.

## How It Works
In the program are a few sample word lists that the user can choose from, though they can also import their own.
The program starts by analyzing the hash to guess what algorithm was used.
These word lists are then read and split into multiple concurrent processes. Each process 'mangles' its entries, generating thousands of variants of each word.
The mangling process is as follows:
- The base case variants are all lowercase, all uppercase, first letter capitalized, and reversed
- The base variants are sent into leet converters, ex: 'e' to '3' or 's' to '$'
- These are sent into common pattern appenders and prependers, ex: password to password123

The processes compare each hash mangled word (using the previously found algorithm) to the original hash to find the solution.

## Technology
- Python multiprocessing
- Python Tkinter
