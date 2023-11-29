import sympy as sp
import random

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

    print("Matrix preparation for transposition:")
    print_matrix(transpose_matrix)

    return transpose_decrypt_result


def matrixToBinary(matrix):
    binary_matrix = [
        [bin(value)[2:] if value is not None else None for value in row]
        for row in matrix
    ]

    return binary_matrix


def vernam_encrypt(transpose_encrypt_result):
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
    print("Vigenere Matrix:")
    for row in vigenere_matrix:
        print(row)
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

    vernam_encrypt_result, otp_matrix_string = vernam_encrypt(transpose_encrypt_result)
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

    with open(f"{fileName}_encrypted.txt", "w") as file:
        file.write(caesar_encrypt_result)

    return caesar_encrypt_result, privateKey, modNum, keyword, otp_matrix_string


def decrypt_my_algo(
    caesar_encrypt_result, privateKey, modNum, keyword, otp_matrix_string, fileToDecrypt
):
    # THIS IS IMPORTANT!! RESET keyword_values
    global keyword_values  # Declare keyword_values as a global variable
    # Reset keyword_values
    keyword_values = []

    privateKey = int(privateKey)
    modNum = int(modNum)

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

    with open(f"{fileToDecrypt}_decrypted.txt", "w") as file:
        file.write(rsa_decrypt_result)


# fileName = "sample"
# with open(f'{fileName}.txt', 'r') as file:
#     message = file.read()

# # # message = "CUS IM NOT A PRINCESS THIS AIN'T A FAIRYTALE"
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


# caesar_cipher = 'CADEF GFCHJ  EEIFC HILHL ILHN NOLGL JHLHM KIMII NOPOL MRRRP NMTLN NNOPP PNMPO QONUT SORV YPQYX TSQTV SaTTW VVZbS XYcXY XVcXd XWcYd adZac aabgZ cbgb iZZZi ___'
# privateKey = 34861
# modNum = 53743
# keyword = 'slayslay!'
# otp_matrix_string = '1011010111 100110010001 101110001001 11000011000 111110111000 101001110 100111010101 110001011110 110010111010 1001010100 100010000101 11000101111 110011100010 1101011110 1110010110 10011110110 111111100011 101010110001 110011011110 100101010010 10011001111 1001100011 10110101011 10110011100 100001111000 111010000 111000111010 ___'
# decrypt_my_algo(caesar_cipher, privateKey, modNum, keyword, otp_matrix_string)

# caesar_cipher = 'BEDBI IHGKH FHGLE KIMJF KJLJL  ILFKH JPPGM KOQLK LNIOQ MOJOS QTTML SSNMS PQVMU RPWSV SSTRV WVSQP  XVZVS WYZTX YXaUa aXWWT bZccb YbeZa cZXbY aaaYX cgdfb fdcZe gcbei hifhd igklk jlhmk hhkji ljflk lmkkj kjhii mokkr mpmsr noslo psmno tqot upowo rtoxw ssppq uysxs xryrv vwvtx  wxAuz Byyyu yBzEw zzAzD AEFGz DEAyB CGzGB DIABG EBIBB HJIDF GGHEL  ______'
# privateKey = 38105
# modNum = 55687
# keyword = '&la5tT3st!'
# otp_matrix_string = '101101010001 111110110001 10111100111 11001010011 10010010001 110000011011 111101 11111011101 1101011101 101111100000 101110100010 11000111 100010000000 111110001001 1100111111 110010111110 101101111001 100110111010 11001000101 111000101101 1111110110 10000111111 11000000110 11100100010 101011001100 110110010000 11100100101 110110100 111011011010 10111011001 11111101100 11001001 111000110001 11001011101 100001101011 10010000011 100001110011 101100111 10110010000 110011101011 110010111011 111010111010 10001001011 110001011011 100011100111 1111110110 100100101000 1110010000 111101010011 10001000101 111001100 110110111010 1101011111 100110011100 1111011110 1101100011 101011110111 100000001110 110111110010 101110010100 ______'
# decrypt_my_algo(caesar_cipher, privateKey, modNum, keyword, otp_matrix_string)

# caesar_cipher = 'HAJGB JJEK CECJ IMLMM JJJE KFKMH NGNKO IMPP MIPKK RSPN OTMSO PLONT VTUM RNSPN QOWP UYYUP WZSWY XaRVW YTaT XcXXb WUWU WZXa cfeee bYZgX cafba daihd ffabd gfiic ggij dkdk lllf jhfmn inho llqk njkkj rjjnn sklsr ruqnt rtmqv ptvq ovur vxtux wtvuu wyAxv stAv wxttu ADACy zvzEA AwEEy DFFCE EFEGC EFFBz EBECA JDGIK DGJ FHHK JNNJJ LLOHN KJGKH LIQJP MIOMJ RMLMR OMLQK QQLNL TUVSP UNOON VOXUO VRVWU XVWYR YZWaS TXba XcbWX ZZWaX bcedW bcabX ZafY chfef bbed fchec hkbgi ghghf ijhgi gihn kfhoh moigj phqjq pqnim qqrkp rqoso ssmuo surms tptsu uttto uvpxp xyryt zstwt zzzwv zxCCt yvvzA ACxvC CEwFE ExDGy EHGzB DzCB EJDBA IKBIC JCKCJ JMKDM JIEFN KNMNL LNHOL NIPNM OPKPK NKLKJ OKMOK RULML RUTUS VPROO VTWWO XVRV WSRSU XaTVZ aTTZV XUXcX abXbX XbXa bYeXc eXfYe feYfg edgdi ggafc gggjk jcilc jlhef klgnj kkfmj kphhh jmop nprri oppjq qrork ppuqu rssvr tvnvw qvts stxwp vwxux vswwA yByyw zCuyx zyuzu AADAv DBCyF ByzDx EDDAB GHHBA GHFIJ BHEB DKDG HEHGM IGGNN JFLFN MOJHH MOOIJ NOMPO OPQKK PMMO ROTQQ SSRNS TQSSW VOOXQ VYRQP SXUY UVZaR XWYUY YZZXZ WWU dVVee cddWe dfedZ ebeaZ dbag ddhch hjgck gckdl jkihl enmk klif hggo mpmi nikpi pqnsk qttln rtuqt nmtp qruqr vutv tqqwv xyrqx xyrwr ________________________________________'
# privateKey = 26783
# modNum = 53743
# keyword = 'lover'
# otp_matrix_string = '11101111111 11111001 101001001010 1001001 11011011110 101011000010 11010011100 110001100001 100000110100 100000110 11001001101 10011010111 110100000 111100001110 11111100101 100001010000 11010100 1111011101 1101000101 11110010001 101110111000 111110000100 10110000011 11010001001 100110010 1001100010 100000001 10001001101 10101101000 100001010110 1101100110 101011011101 100111001000 100001010101 110101001011 10001001110 111100101 1000111100 100101110001 110101001111 110000010001 1100011101 10000110 100011011100 101000110011 1111011001 101000101010 10001010001 10100001101 111100111001 101010100100 11100001111 100011101100 111001001101 110001100010 100010011001 10001 1001010 11011110101 1001001110 110001101 101101001011 11001111100 111110110 101011110011 10010001100 111100100000 1001110110 1101110100 100011000010 100100001000 110010110110 11110110011 101111011011 1101011101 100010000001 110101111001 110010011000 101101100110 1111101001 101101101111 1010001011 100011110001 100110101010 110100010011 10001011111 111111010111 111011011000 11110011111 110010101000 11000011100 10001010110 100010100110 110010111100 100100110000 10100111110 101101101000 101011010110 111110010110 111001101111 101110 111000110011 1101011001 101010011001 1100111010 11110010100 11100111111 1011110001 10111100011 101001110110 110001011011 11010001000 100100001000 11010110101 101110000101 10000101000 101001110110 111000000011 101101 111000110100 101110010000 11000000 10111001111 10100001 100101101101 100101110010 101100100110 11101000101 1100011110 10001101101 1110010 11010011111 11001101100 110111100000 100100100011 10110011111 110010010010 100001000011 101001010110 1001010111 100111011000 100101000001 1000101011 100001 111010001100 1001111010 1110011111 1100000 1001100000 1100110 10100100100 110001110 11001010101 11101011000 100001100101 110000001100 101001000101 11000010010 100100001001 101101111011 101111101101 10101100110 110110000101 110011000101 1100100110 110001000101 11000111111 11110001011 110010000110 1110101 11111110100 100001000 101000100110 101011111110 10111110000 1111111010 1111100111 101011011000 101100100000 111011011110 111001001 10001110110 101011001 111001001111 11000111001 1001000010 100100011100 110111001110 110101101011 110100011011 100110010000 100111101101 101111100011 111110100010 100110111101 10101001000 100111111011 101001110000 111110000111 10001000010 ________________________________________'
# decrypt_my_algo(caesar_cipher, privateKey, modNum, keyword, otp_matrix_string)

# caesar_cipher = 'EDJAB GIIEJ FLKFH GMKIK IFHHI KKLOL JOOPH LHJPM LQLJI OOJRK PRQST QNOPM QUSV OVSOO RWUUO VQRTX VWYVQ UZTaY XUZZb XUaXb abbaY aZXYc bcZff aXcaZ cZcdd ciaic fiigg ekcfc ijfhj ijfkl heknn imhmk llnkh mmkhp mrkrk  pljkl prss otrot qnqop qnrnp sxsxs swwxp vxzqq wytwr yzttt wBCAu Avuy yBAwy zFyAy DABxG DyCAy FCGID FIBIG _________'
# privateKey = 24331
# modNum = 47053
# keyword = 'taylor'
# otp_matrix_string = '1000101110 11110110101 100100111001 111100011100 111100100100 111100010111 10100110011 110001101 101001000011 1100111011 100101111001 110001100111 100010111100 110001100010 1000001010 11010001011 111000111010 111011010000 111110110011 111000010100 1111000100 1001001 110001101111 101000010111 111100101001 100000001101 1001111011 100011010001 10100100101 100011011100 101000111101 1110000101 1011100111 110000110111 101010000001 10001010000 1110000000 10011110 101000011001 1011011001 101101111000 1100110000 110011010 101001000100 11011001 110000101 101000011 100100100100 1000111000 100001111100 110110011101 1011101 110011110010 1100111011 _________'
# decrypt_my_algo(caesar_cipher, privateKey, modNum, keyword, otp_matrix_string)

# caesar_cipher = 'EDJAB GIIEJ FLKFH GMKIK IFHHI KKLOL JOOPH LHJPM LQLJI OOJRK PRQST QNOPM QUSV OVSOO RWUUO VQRTX VWYVQ UZTaY XUZZb XUaXb abbaY aZXYc bcZff aXcaZ cZcdd ciaic fiigg ekcfc ijfhj ijfkl heknn imhmk llnkh mmkhp mrkrk  pljkl prss otrot qnqop qnrnp sxsxs swwxp vxzqq wytwr yzttt wBCAu Avuy yBAwy zFyAy DABxG DyCAy FCGID FIBIG _________'
# privateKey = 24331
# modNum = 47053
# keyword = 'taylor'
# otp_matrix_string = '1000101110 11110110101 100100111001 111100011100 111100100100 111100010111 10100110011 110001101 101001000011 1100111011 100101111001 110001100111 100010111100 110001100010 1000001010 11010001011 111000111010 111011010000 111110110011 111000010100 1111000100 1001001 110001101111 101000010111 111100101001 100000001101 1001111011 100011010001 10100100101 100011011100 101000111101 1110000101 1011100111 110000110111 101010000001 10001010000 1110000000 10011110 101000011001 1011011001 101101111000 1100110000 110011010 101001000100 11011001 110000101 101000011 100100100100 1000111000 100001111100 110110011101 1011101 110011110010 1100111011 _________'
# decrypt_my_algo(caesar_cipher, privateKey, modNum, keyword, otp_matrix_string)

# fileToDecrypt = "sample"
# with open(f"{fileToDecrypt}_encrypted.txt", "r") as file:
#     message = file.read()
# caesar_cipher = message
# privateKey = 1271
# modNum = 55189
# keyword = "taylor"
# otp_matrix_string = "110100011111 110110010100 10110011 1101010100 101010001111 101111010000 100110001 111101001001 11000110000 1100000010 110100011 11100011 111001101010 110110111011 101011110111 1110011111 10100100011 1100101100 110010011111 1000100001 110110101000 110101101110 11001111 1111101100 111011110011 110111110101 111000101001 11101111 101010010010 10111010111 10011011100 101000100100 111010110001 10101111010 100001001010 101100111011 111001010110 11101111111 111101101 110000000111 101101111010 1101100110 100101 101110011110 101101100110 10010001110 101010000111 101000011110 1010000010 101010000001 10111100011 10001 110101100001 100101100011 10010001100 110001101110 10100110100 11011101110 1001110001 100101010100 110011001001 100000111000 100111110101 110110 111100100100 100010 ___________"
# decrypt_my_algo(
#     caesar_cipher, privateKey, modNum, keyword, otp_matrix_string, fileToDecrypt
# )

# fileToDecrypt = "sample"
# with open(f"{fileToDecrypt}_encrypted.txt", "r") as file:
#     message = file.read()
# caesar_cipher = message
# privateKey = 973
# modNum = 53743
# keyword = "taylor"
# otp_matrix_string = "11111011010 110001001100 10010011 1100101101 111010111011 111001110111 111110111100 101010000111 111001111 111011100110 1011011111 101101100000 111011111 10111010101 110100100110 11100111110 11111111101 11110010100 1001101111 101101 11011110000 111010010100 101111001101 1000111011 110011100001 11001110010 100101101101 101100110101 10110001101 101000001001 11001110011 101011111110 100010100 101010100011 1001111110 101101111010 100101101111 111000010111 111101111001 111000101001 110100001111 110111101010 111100100010 100010100100 11100010011 100100110001 111110000110 11110101010 101001111111 110101111111 1111 111100000101 110101001000 10000011110 110010010 1010011110 110000111000 111011100011 1111110011 110000110000 10011001 11010001011 10100000001 11111100010 100001 111100110111 ___________"
# decrypt_my_algo(
#     caesar_cipher, privateKey, modNum, keyword, otp_matrix_string, fileToDecrypt
# )
