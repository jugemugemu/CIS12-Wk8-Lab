from numpy import mod, add, subtract # Is this worth using for this project?
from os import system, name # I thought I would try
from sys import exit

def vigenere_sq_header(alphabet:str) -> list:
    return list(' ') + list(alphabet)

def vigenere_sq(alphabet:str) -> list:
    alphabet = list(alphabet)
    sq_list = [vigenere_sq_header(alphabet)]
    for i in range(len(alphabet)):
        sq_list.append(list(alphabet[i]) + alphabet[i:] + alphabet[:i])
    return sq_list

def vigenere_sq_print(sq_list:list):
    for i, row in enumerate(sq_list):
        print(f'| {' | '.join(row)} |')
        if i == 0:
            print(f'{'|---' * len(row)}|')

def char_to_index(character:str, alphabet:str) -> int:
    return alphabet.find(character)

def index_to_char(index:int, alphabet:str) -> str:
    if 0 <= index <= len(alphabet):
        return alphabet[index]

def vigenere_index(key_char:str, plaintext_char:str, alphabet:str) -> str:
    return index_to_char(
        mod( # Calculates the index for the encrypted character
            add(
                char_to_index(plaintext_char, alphabet),
                char_to_index(key_char, alphabet)
            ), len(alphabet)
        ), alphabet
    )

def undo_vigenere_index(key_char:str, ciphertext_char:str, alphabet:str) -> str:
    return index_to_char(
        mod( # Calculates the index of the decrypted character
            subtract(
                char_to_index(ciphertext_char, alphabet),
                char_to_index(key_char, alphabet)
            ),
            len(alphabet)
        ),
        alphabet
    )

def encrypt_vigenere(key:str, plaintext:str, alphabet:str) -> str:
    ciphertext = []
    for i, c in enumerate(plaintext):
        ciphertext.append(vigenere_index(key[mod(i, len(key))], c, alphabet))
    return ''.join(ciphertext)

def decrypt_vigenere(key:str, ciphertext:str, alphabet:str) -> str:
    plaintext = []
    for i, c in enumerate(ciphertext):
        plaintext.append(undo_vigenere_index(key[mod(i, len(key))], c, alphabet))
    return ''.join(plaintext)

def in_alphabet(text:str, alphabet:str) -> bool:
    for c in text:
        if c not in alphabet:
            return False
    return True

def enc_menu(key:str, alphabet:str, ciphertext_list) -> int:
    print('VIGENERE MENU > ENCRYPT')
    plaintext = input('Enter the plaintext to be encrypted:\n> ')
    if in_alphabet(plaintext, alphabet):
        ciphertext_list.append(encrypt_vigenere(key, plaintext, alphabet))
        return 3 # Encryption ran successfully
    return 4 # Encryption failed: plaintext contains chars not in alphabet

def dec_menu(key:str, alphabet:str, ciphertext_list:list):
    print('VIGENERE MENU > DECRYPT')
    for ciphertext in ciphertext_list:
        print(decrypt_vigenere(key, ciphertext, alphabet))

    input('Press ENTER to return to main menu')
    return 0 # No error/message to display

def dec_dump_menu(ciphertext_list:list):
    print('VIGENERE MENU > CIPHERTEXT DUMP')
    for ciphertext in ciphertext_list:
        print(ciphertext)

    input("Press ENTER to return to main menu")
    return 0 # No error/message to display

def main():
    # Detect OS and prepare associated terminal clearing command
    commands = ['cls', 'clear']
    os_id = 1
    if name == 'nt':
        os_id = 0
    elif name == 'posix':
        os_id = 1

    # Alphabets to use
    ALPHABET = 'abcdefghijklmnopqrstuvwxyz'
    NUMBERS = '0123456789'
    SPECIAL_CHARS = ' .,?!@#$%^&*'
    alphabet_cust1 = ALPHABET + ALPHABET.upper() + ' '

    ciphertext_list = []

    key = 'DAVINCI'

    # Menu options and what they do
    menu = [
        ['[1] Encrypt', enc_menu, [key, alphabet_cust1, ciphertext_list]],
        ['[2] Decrypt', dec_menu, [key, alphabet_cust1, ciphertext_list]],
        ['[3] Dump Encrypted', dec_dump_menu, [ciphertext_list]],
        ['[4] Exit', exit, [0]]
    ]

    # Types of errors/messages that can be displayed
    msg = [
        '',
        '\nImproper choice',
        '\nImproper choice: enter integer between 1 and 4',
        '\nEncryption ran successfully',
        '\nEncryption failed: plaintext contains chars not in alphabet'
    ]
    msg_id = 0

    while True:
        system(commands[os_id]) # Clear the terminal
        # Print the menu options
        print(f'VIGENERE MENU {msg[msg_id]}')
        print('Enter the number of one of the options below:')
        for option in menu:
            print(option[0])

        try:
            choice = int(input('> '))
            if not (0 <= choice <= len(menu)):
                msg_id = 1 # Improper choice
            else:
                system(commands[os_id]) # Clear the terminal
                msg_id = menu[choice-1][1](*menu[choice-1][2])
        except ValueError as ignored:
            msg_id = 2 # Improper choice: enter integer between 1 and 4

if __name__ == '__main__':
    main()

    # TESTS
    #vigenere_sq_print(vigenere_sq(alphabet_cust2))
    #print(vigenere_index())
    #print(vigenere_index('b', 'b', alphabet))
    #print(undo_vigenere_index('b', 'c', alphabet))
    #print(encrypt_vigenere(key, plaintext, alphabet_cust1))
    #print(decrypt_vigenere(key, encrypt_vigenere(key, plaintext, alphabet_cust1), alphabet_cust1))


