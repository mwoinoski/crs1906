# simple_crypt.py encrypts a string using a simple substitution cipher.
# Not suitable for production use ;)

import string


def main():
    shift = 3
    choice = input("Would you like to encode or decode?")
    word = input("Please enter text")
    letters = string.ascii_letters + string.punctuation + string.digits
    encoded = ''
    if (choice == "encode"):
        for letter in word:
            if letter == ' ':
                encoded = encoded + ' '
            else:
                x = letters.index(letter) + shift
                encoded = encoded + letters[x]
    if choice == "decode":
        for letter in word:
            if letter == ' ':
                encoded = encoded + ' '
            else:
                x = letters.index(letter) - shift
                encoded = encoded + letters[x]

    print(encoded)


if __name__ == '__main__':
    main()