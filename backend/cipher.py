# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def encrypt(inputText, N, D):
    if D != -1 and D != 1:
        print('invalid entry, cannot encrypt! Try entering a value 1 or -1 for D')
        return

    if N < 1:
        print('invalid entry, cannot encrypt! Try entering a value greater than or equal to 1 for N')

    inputText = inputText[::-1]

    inputASCII = []
    for char in inputText:
        inputASCII.append(ord(char))
    count = 0
    for val in inputASCII:
        if val == 31 or val == 32:
            print('invalid entry, cannot encrypt! Try using no spaces or exclamation marks')
            return
        if D > 0:
            if val + N > 126:
                temp = val + N - 126
                val = 34 + temp
            else:
                val += N
        else:
            if val - N < 34:
                temp = val - N
                temp = 34 - temp
                val = 126 - temp
            else:
                val -= N
        inputASCII[count] = val
        count = count+1

    encrypted_string = ''
    for i in range(len(inputASCII)):
        encrypted_string += chr(inputASCII[i])
    return encrypted_string


def decrypt(inputText, N, D):
    if D != -1 and D != 1:
        print('invalid entry, cannot decrypt! Try entering a value 1 or -1 for D')
        return

    if N < 1:
        print('invalid entry, cannot decrypt! Try entering a value greater than or equal to 1 for N')

    inputASCII = []
    for char in inputText:
        inputASCII.append(ord(char))
    count = 0
    for asci in inputASCII:
        if asci == 31 or asci == 32:
            print('invalid entry, cannot decrypt! Try using no spaces or exclamation marks')
            return
        if D < 0:
            if asci + N > 126:
                temp = asci + N - 126
                val = 34 + temp
            else:
                asci += N
        else:
            if asci - N < 34:
                temp = asci - N
                temp = 34 - temp
                asci = 126 - temp
            else:
                asci -= N
        inputASCII[count] = asci
        count = count + 1
    decrypted_string = ''
    for intger in inputASCII:
        decrypted_string += chr(intger)
    decrypted_string = decrypted_string[::-1]
    return decrypted_string


# def test_task_3():
#     file = open('database.txt', 'r')
#     for line in file:
#         userpswd = line.split(" ")
#         userpswd[1] = userpswd[1].rstrip('\n')
#         print(decrypt(userpswd[0], 3, 1) + " " + decrypt(userpswd[1], 3, 1))
#         print()
#
#
# test_task_3()

# Question 1: asamant/Temp123, skharel/Life15$ are the only two combinations present in the database
#
# Question 2: bjha, aissa are the only two usernames that are in the table but do not have their corresponding passwords
#             in the database
#
# Question 3: Ally! does not meet the requirements because there is an exclamation mark
