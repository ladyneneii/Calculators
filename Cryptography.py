import sympy as sp
import random
import io
import os

# stores all the indices in the order of the ASCII value of their assigned letter in the keyword, to be used in transpositional and vigenere encryption and decryption
keyword_values = []
# creating the vigenere matrix
vigenere_matrix = [[(row + col) % 10 for col in range(10)] for row in range(10)]
# creating the caesar cipher
caesar_guide = [
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
]

# Print the result
# print(caesar_guide)


def rsa_encrypt(message):
    ### DEFINING NECESSARY VARIABLES
    prime1 = sp.randprime(200, 250)
    prime2 = sp.randprime(200, 250)
    # prime1 = 7
    # prime2 = 19

    if prime2 == prime1:
        prime2 = sp.randprime(251, 300)

    modNum = prime1 * prime2
    totientNum = (prime1 - 1) * (prime2 - 1)

    # Getting the value of public key
    eCandidates = list(sp.primerange(2, totientNum))
    publicKey = random.choice(eCandidates)

    # Getting the value of the private key
    privateKey = result = 0
    while result != 1:
        privateKey += 1
        result = privateKey * publicKey % totientNum

    # print(prime1, prime2, modNum, totientNum)
    # print(f"prime1 = {prime1}")
    # print(f"prime2 = {prime2}")
    # print(f"modNum = {modNum}")
    # print(f"totientNum = {totientNum}")
    # # print(f"eCandidates = {eCandidates}")
    # print(f"publicKey = {publicKey}")
    # print(f"privateKey = {privateKey}")

    ### ENCRYPTION
    rsa_encrypt_result = []
    for idx in range(len(message)):
        rsa_encrypt_result.append(pow(ord(message[idx]), publicKey, modNum))

    return rsa_encrypt_result, privateKey, modNum


def rsa_decrypt(transpose_decrypt_result, privateKey, modNum):
    ### DECRYPTION
    rsa_decrypt_result = []
    for idx in range(len(transpose_decrypt_result)):
        rsa_decrypt_result.append(
            pow(transpose_decrypt_result[idx], privateKey, modNum)
        )
        rsa_decrypt_result[idx] = chr(rsa_decrypt_result[idx])

    # else:
    #     print("Private key does not exist.")
    print(f"rsa_decrypt_result character list: {rsa_decrypt_result}")
    rsa_decrypt_result = "".join(rsa_decrypt_result)

    return rsa_decrypt_result


def create_char_index(keyword):
    char_index = {}
    for idx in range(len(keyword)):
        character = keyword[idx]
        if character in char_index:
            char_index[character].append(idx)
        else:
            char_index[character] = [idx]

    sorted_char_index = dict(sorted(char_index.items()))
    print(char_index)
    print(sorted_char_index)
    print()

    return sorted_char_index


def transpositional_encrypt(rsa_encrypt_result, keyword):
    # creating the matrix
    cols = len(keyword)
    transpose_matrix = []
    transpose_matrix = [
        list(rsa_encrypt_result[i : i + cols])
        for i in range(0, len(rsa_encrypt_result), cols)
    ]
    print("Matrix preparation for transposition:")
    print("transpose_matrix:")
    print_matrix(transpose_matrix)

    # creating the char_index to get the index associated with a letter in the keyword
    sorted_char_index = create_char_index(keyword)

    # Iterate through values in key-value pairs
    transpose_encrypt_result = []
    for indices_list in sorted_char_index.values():
        for idx in indices_list:
            # Get all values in the idx column (index idx)
            transpose_encrypt_result.append(
                [row[idx] if len(row) > idx else None for row in transpose_matrix]
            )
            keyword_values.append(idx)

    # print(f"matrix {matrix}")
    # print(f"sorted_char_index {sorted_char_index}")
    # print(f"transpose_encrypt_result {transpose_encrypt_result}")
    return transpose_encrypt_result, keyword


def transpositional_decrypt(vernam_decrypt_result):
    # Get the number of rows and columns of the vernam_decrypt_result matrix
    num_rows = len(vernam_decrypt_result)
    num_columns = len(vernam_decrypt_result[0])

    # Initialize the transpose_matrix matrix
    transpose_matrix = [["" for _ in range(num_rows)] for _ in range(num_columns)]
    idx = 0

    for list in vernam_decrypt_result:
        col = keyword_values[idx]
        for row in range(len(list)):
            transpose_matrix[row][col] = list[row]
        idx += 1

    # combine the matrix into one list excluding None
    transpose_decrypt_result = [
        element for row in transpose_matrix for element in row if element is not None
    ]

    print("Matrix preparation for transposition")
    print("transpose_matrix:")
    print_matrix(transpose_matrix)

    return transpose_decrypt_result


def matrixToBinary(matrix):
    binary_matrix = [
        [bin(value)[2:] if value is not None else None for value in row]
        for row in matrix
    ]

    return binary_matrix


def vernam_encrypt(transpose_encrypt_result, fileName):
    # convert the values in the transpose_encrypt_result to binary
    binary_matrix = matrixToBinary(transpose_encrypt_result)

    print("binary_matrix:")
    print_matrix(binary_matrix)

    # Get the number of rows and columns of the binary_matrix
    num_rows = len(binary_matrix)
    num_columns = len(binary_matrix[0])

    # Decide the number of bits the values in the OTP must have
    num_bits = 12

    # Generate an OTP matrix with random values
    otp_matrix = [
        [bin(random.getrandbits(num_bits))[2:] for _ in range(num_columns)]
        for _ in range(num_rows)
    ]

    print("otp_matrix:")
    print_matrix(otp_matrix)

    # Perform XOR operation between corresponding values in binary_matrix and otp_matrix
    vernam_encrypt_result = [
        [
            int(binary_elem, 2) ^ int(otp_elem, 2) if binary_elem is not None else None
            for binary_elem, otp_elem in zip(binary_row, otp_row)
        ]
        for binary_row, otp_row in zip(binary_matrix, otp_matrix)
    ]

    # convert otp_matrix to a single string for user display
    num_cols = len(otp_matrix[0])
    otp_matrix_string = ""

    for row in otp_matrix:
        for col in row:
            if col:
                otp_matrix_string += "".join(col) + " "
            else:
                otp_matrix_string += " "

    # number of underscores correspond to the number of columns
    otp_matrix_string += "_" * num_cols

    # # output a separate OTP file in case the otp is too long
    # print("helloooo")
    # with open(f"{fileName}_otp.txt", "w") as file:
    #     file.write(otp_matrix_string)

    return vernam_encrypt_result, otp_matrix_string


def vernam_decrypt(vigenere_decrypt_result, otp_matrix_string):
    # Count underscores at the end
    count_underscores = 0
    for char in reversed(otp_matrix_string):
        if char == "_":
            count_underscores += 1
        else:
            break

    otp_matrix = []
    row = []
    col_count = 0

    # convert the otp_matrix_string string into a matrix for user display
    current_group = ""
    for char in otp_matrix_string:
        if char == "_":
            break
        if char == " ":
            if current_group:
                row.append(current_group)
                current_group = ""
            else:
                row.append(None)
            col_count += 1
            if col_count == count_underscores:
                otp_matrix.append(row)
                row = []
                col_count = 0
        else:
            current_group += char

    print("otp_matrix:")
    print_matrix(otp_matrix)

    vernam_decrypt_result = [
        [
            int(bin(XOR_elem)[2:], 2) ^ int(otp_elem, 2)
            if XOR_elem is not None
            else None
            for XOR_elem, otp_elem in zip(XOR_row, otp_row)
        ]
        for XOR_row, otp_row in zip(vigenere_decrypt_result, otp_matrix)
    ]

    return vernam_decrypt_result


def vigenere_encrypt(vernam_encrypt_result):
    print("vigenere_matrix:")
    print_matrix(vigenere_matrix)
    # print("XOR Matrix:")
    # for row in vernam_encrypt_result:
    #     print(row)

    vigenere_encrypt_result = vernam_encrypt_result

    vigenere_shift = 0
    for depth_num in range(len(vigenere_encrypt_result)):
        for row_num in range(len(vigenere_encrypt_result[depth_num])):
            # check if it is a None
            if vigenere_encrypt_result[depth_num][row_num]:
                # Convert the number to a string then to a list to allow item assignment
                XOR_row_list = list(str(vigenere_encrypt_result[depth_num][row_num]))
                col_num = 0
                while col_num < len(XOR_row_list):
                    col = int(XOR_row_list[col_num])
                    row = keyword_values[
                        (col_num + vigenere_shift) % len(keyword_values)
                    ]
                    XOR_row_list[col_num] = str(vigenere_matrix[row][col])
                    col_num += 1
                vigenere_shift = col_num
                # Convert the list back to a string
                vigenere_encrypt_result[depth_num][row_num] = "".join(XOR_row_list)

    print(f"keyword_values {keyword_values}")

    return vigenere_encrypt_result


def vigenere_decrypt(caesar_decrypt_result, keyword):
    sorted_char_index = create_char_index(keyword)

    # Iterate through values in key-value pairs
    for indices_list in sorted_char_index.values():
        for idx in indices_list:
            keyword_values.append(idx)

    vigenere_decrypt_result = caesar_decrypt_result
    print("Vigenere Matrix:")
    print_matrix(vigenere_matrix)
    print(f"keyword_values {keyword_values}")

    vigenere_shift = 0
    for depth_num in range(len(vigenere_decrypt_result)):
        for row_num in range(len(vigenere_decrypt_result[depth_num])):
            # check if it is a None
            if vigenere_decrypt_result[depth_num][row_num]:
                # Convert the string to a list to allow item assignment
                vigenere_row_list = list(vigenere_decrypt_result[depth_num][row_num])
                col_num = 0
                while col_num < len(vigenere_row_list):
                    intersect_value = int(vigenere_row_list[col_num])
                    row = keyword_values[
                        (col_num + vigenere_shift) % len(keyword_values)
                    ]

                    for col in range(len(vigenere_matrix[row])):
                        if vigenere_matrix[row][col] == intersect_value:
                            vigenere_row_list[col_num] = str(col)
                            break

                    col_num += 1
                vigenere_shift = col_num
                # Convert the list back to a string then to decimal
                vigenere_decrypt_result[depth_num][row_num] = int(
                    "".join(vigenere_row_list)
                )

    return vigenere_decrypt_result


def caesar_encrypt(vigenere_encrypt_result):
    print(f"caesar_guide: {caesar_guide}")
    print()

    caesar_matrix = vigenere_encrypt_result
    caesar_shift = 0
    for depth_num in range(len(caesar_matrix)):
        for row_num in range(len(caesar_matrix[depth_num])):
            # check if it is a None
            if caesar_matrix[depth_num][row_num]:
                # Convert the string to a list to allow item assignment
                XOR_row_list = list(caesar_matrix[depth_num][row_num])
                col_num = 0
                while col_num < len(XOR_row_list):
                    col = int(XOR_row_list[col_num])
                    XOR_row_list[col_num] = caesar_guide[
                        (col + caesar_shift) % len(caesar_guide)
                    ]
                    col_num += 1
                caesar_shift += 1
                # Convert the list back to a string
                caesar_matrix[depth_num][row_num] = "".join(XOR_row_list)

    print("caesar_matrix:")
    print_matrix(caesar_matrix)

    # convert matrix to a single string for user display
    num_cols = len(caesar_matrix[0])
    caesar_encrypt_result = ""

    for row in caesar_matrix:
        for col in row:
            if col:
                caesar_encrypt_result += "".join(col) + " "
            else:
                caesar_encrypt_result += " "

    # number of underscores correspond to the number of columns
    caesar_encrypt_result += "_" * num_cols

    return caesar_encrypt_result


def caesar_decrypt(caesar_encrypt_result):
    # Count underscores at the end
    count_underscores = 0
    for char in reversed(caesar_encrypt_result):
        if char == "_":
            count_underscores += 1
        else:
            break

    caesar_matrix = []
    row = []
    col_count = 0

    # convert the caesar_encrypt_result string into a matrix
    current_group = ""
    for char in caesar_encrypt_result:
        if char == "_":
            break
        if char == " ":
            if current_group:
                row.append(current_group)
                current_group = ""
            else:
                row.append(None)
            col_count += 1
            if col_count == count_underscores:
                caesar_matrix.append(row)
                row = []
                col_count = 0
        else:
            current_group += char

    print("caesar_matrix:")
    print_matrix(caesar_matrix)

    print(f"caesar_guide: {caesar_guide}")
    print()

    caesar_decrypt_result = caesar_matrix
    caesar_shift = 0
    for depth_num in range(len(caesar_decrypt_result)):
        for row_num in range(len(caesar_decrypt_result[depth_num])):
            # check if it is a None
            if caesar_decrypt_result[depth_num][row_num]:
                # Convert the string to a list to allow item assignment
                XOR_row_list = list(caesar_decrypt_result[depth_num][row_num])
                col_num = 0
                while col_num < len(XOR_row_list):
                    col = str(
                        (caesar_guide.index(XOR_row_list[col_num]) - caesar_shift)
                        % len(caesar_guide)
                    )
                    XOR_row_list[col_num] = col
                    col_num += 1
                caesar_shift += 1
                # Convert the list back to a string
                caesar_decrypt_result[depth_num][row_num] = "".join(XOR_row_list)

    return caesar_decrypt_result


def print_matrix(matrix):
    for row in matrix:
        print(row)


def encrypt_my_algo(message, keyword, fileName):
    # THIS IS IMPORTANT!! RESET keyword_values
    global keyword_values  # Declare keyword_values as a global variable
    # Reset keyword_values
    keyword_values = []

    print()
    print("SAMPLE ENCRYPTION OUTPUT IN THE TERMINAL ONLY")
    print(f"Message to encrypt: {message}")
    print()

    # ENCRYPT
    rsa_encrypt_result, privateKey, modNum = rsa_encrypt(message)
    print(f"rsa_encrypt_result: {rsa_encrypt_result}")
    print()

    transpose_encrypt_result, keyword = transpositional_encrypt(
        rsa_encrypt_result, keyword
    )
    print("transpose_encrypt_result:")
    print_matrix(transpose_encrypt_result)
    print()

    vernam_encrypt_result, otp_matrix_string = vernam_encrypt(
        transpose_encrypt_result, fileName
    )
    print("vernam_encrypt_result:")
    print_matrix(vernam_encrypt_result)
    print()

    vigenere_encrypt_result = vigenere_encrypt(vernam_encrypt_result)
    print("vigenere_encrypt_result:")
    print_matrix(vigenere_encrypt_result)
    print()

    caesar_encrypt_result = caesar_encrypt(vigenere_encrypt_result)
    print(f"caesar_encrypt_result: {caesar_encrypt_result}")
    print()

    download_link = f'<a href="data:text/plain;charset=utf-8,{caesar_encrypt_result}" download="{fileName}_encrypted.txt">Download File</a>'
    print(download_link)

    download_link_href = f"data:text/plain;charset=utf-8,{caesar_encrypt_result}"
    download_link_download = f"{fileName}_encrypted.txt"

    print("Save these information:")
    print(f"Private Key: {privateKey}")
    print(f"Mod: {modNum}")
    print(f"Keyword: {keyword}")
    print(f"OTP: {otp_matrix_string}")

    return (
        caesar_encrypt_result,
        privateKey,
        modNum,
        keyword,
        otp_matrix_string,
        download_link_href,
        download_link_download,
    )


def decrypt_my_algo(
    caesar_encrypt_result, privateKey, modNum, keyword, otp_matrix_string, fileToDecrypt
):
    # THIS IS IMPORTANT!! RESET keyword_values
    global keyword_values  # Declare keyword_values as a global variable
    # Reset keyword_values
    keyword_values = []

    privateKey = int(privateKey)
    modNum = int(modNum)

    print()
    print("SAMPLE DECRYPTION OUTPUT IN THE TERMINAL ONLY")
    print(f"Cipher to decrypt: {caesar_encrypt_result}")
    print()

    # DECRYPT
    caesar_decrypt_result = caesar_decrypt(caesar_encrypt_result)
    print("caesar_decrypt_result:")
    print_matrix(caesar_decrypt_result)
    print()

    vigenere_decrypt_result = vigenere_decrypt(caesar_decrypt_result, keyword)
    print("vigenere_decrypt_result:")
    print_matrix(vigenere_decrypt_result)
    print()

    vernam_decrypt_result = vernam_decrypt(vigenere_decrypt_result, otp_matrix_string)
    print("vernam_decrypt_result:")
    print_matrix(vernam_decrypt_result)
    print()

    transpose_decrypt_result = transpositional_decrypt(vernam_decrypt_result)
    print(f"transpose_decrypt_result: {transpose_decrypt_result}")
    print()

    rsa_decrypt_result = rsa_decrypt(transpose_decrypt_result, privateKey, modNum)
    print(f"rsa_decrypt_result: {rsa_decrypt_result}")
    print()

    download_link_href = f"data:text/plain;charset=utf-8,{rsa_decrypt_result}"
    download_link_download = f"{fileToDecrypt}_decrypted.txt"

    return download_link_href, download_link_download


# fileName = "myname"
# with open(f'{fileName}.txt', 'r') as file:
#     message = file.read()

# keyword = "taylor"
# if len(keyword) <= 10:
#     caesar_cipher, privateKey, modNum, keyword, otp_matrix_string = encrypt_my_algo(message, keyword, fileName)
#     print("Message:")
#     print(message)
#     print("Cipher:")
#     print(caesar_cipher)
#     print("Private Key:")
#     print(privateKey)
#     print("Mod:")
#     print(modNum)
#     print("Keyword:")
#     print(keyword)
#     print("OTP Number:")
#     print(otp_matrix_string)
# else:
#     print("keyword should only contain up to 10 characters.")


# fileToDecrypt = "myname_encrypted"
# caesar_cipher = "FGGED EEKE DELHF JFJFL INHEK KGFIF LLHGK  OIOPN NJQMP PRMRN  RMLTM PQLNL TQVO  RWUTU RPQQR VSRRX RUYQ VXYST YVWUT YTVbU  ____"
# privateKey = 37199
# modNum = 50621
# keyword = "CS-3104"
# otp_matrix_string = "101010101111 101000110100 101110100110 10100110001 11101000110 101000111100 100100110101 110010010100 101100000101 1100001000 100010011100 101000011111 101110100101 10000010101 __"
# decrypt_my_algo(
#     caesar_cipher, privateKey, modNum, keyword, otp_matrix_string, fileToDecrypt
# )
