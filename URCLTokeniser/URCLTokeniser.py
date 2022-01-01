
# input fileName

# read file

# clean code
    # 1 delete multiline comments
    # 2 delete line comments
    # 3 delete empty lines
    # 4 convert double spaces to single spaces

# find headers
    # 1 find BITS
    # 2 find MINREG
    # 3 find MINHEAP
    # 4 find MINSTACK
    # 5 find RUN
        # store each value and delete afterwards
    # headers = (BITS, bitOperator, MINREG, MINHEAP, MINSTACK, RUN)

# tokens = []
# for line in file:
    # index = 0
    # token = []
    # while index < len(line):
        # if line[index].isalpha():
            # text = ""
            # while line[index].isalpha():
                # text += line[index]
                # index += 1
            # token.append(text)
        # elif line[index].isnumeric():
            # number = ""
            # while (line[index].isalpha()) or (line[index] in ["x", "X", "o", "O", "d", "D"]):
                # number += line[index]
                # index += 1
            # token.append(number)
        # elif line[index] in ("[", "]"):
            # token.append(line[index])
            # index += 1
        # else:
            # raise Exception(f"FATAL - Unrecognised symbol: {line[index]}")

# return tokens, headers

#################################################################################################
#################################################################################################
#################################################################################################

# input fileName
def URCLTokeniser(fileName: str = "input.urcl", offline: bool = "True") -> tuple[list, tuple]:
    """
    Takes raw input URCL code.
    
    Returns tokenised URCL and tuple with header information.
    """
    
    # read file
    if offline:
        f = open(fileName, "r")
        file = f.read()
        f.close()
    else:
        file = fileName
    
    # clean code
    # 1 delete multiline comments
    while file.find("/*") != -1:
        index1 = file.index("/*")
        index2 = file.index("*/") + 2
        file = file[: index1] + file[index2: ]
    
    # 2 delete line comments
    file = file.splitlines()
    for line in range(len(file)):
        if file[line].find("//") != -1:
            file[line] = file[line][: file[line].index("//")]
    
    # 3 delete empty lines
    index = 0
    while index < len(file):
        if not(file[index]):
            file.pop(index)
        else:
            index += 1
    
    # 4 convert double spaces to single spaces
    for line in range(len(file)):
        while file[line].find("  ") != -1:
            file[line] = file[line].replace("  ", " ")
    
    # find headers
    BITS = 8
    bitOperator = "=="
    MINREG = 8
    MINHEAP = 16
    MINSTACK = 8
    RUN = "ROM"
    line = 0
    while line < len(file):
        # 1 find BITS
        if file[line].startswith("BITS"):
            token = file[line].split(" ")
            if len(token) == 3:
                BITS = int(token[2], 0)
                bitOperator = token[1]
            elif len(token) == 2:
                BITS = int(token[1], 0)
                bitOperator = "=="
            else:
                raise Exception("FATAL - Incorrect number of operands for BITS header")
            file.pop(line)
        # 2 find MINREG
        elif file[line].upper().startswith("MINREG"):
            MINREG = int(file[line][7: ], 0)
            file.pop(line)
        # 3 find MINHEAP
        elif file[line].upper().startswith("MINHEAP"):
            MINHEAP = int(file[line][8: ], 0)
            file.pop(line)
        # 4 find MINSTACK
        elif file[line].upper().startswith("MINSTACK"):
            MINSTACK = int(file[line][9: ], 0)
            file.pop(line)
        # 5 find RUN
        elif file[line].upper().startswith("RUN"):
            RUN = file[line][4: ].upper()
            file.pop(line)
        else:
            line += 1
    # store each value and delete afterwards
    # headers = (BITS, bitOperator, MINREG, MINHEAP, MINSTACK, RUN)
    headers = (BITS, bitOperator, MINREG, MINHEAP, MINSTACK, RUN)
            
    # tokenise
    tokens = []
    for line in file:
        index = 0
        token = []
        while index < len(line):
            if (line[index].isalpha()) or (line[index].isnumeric()) or (line[index] in ("&", "%", "#", ".", "$", "~", "-")):
                if line[index] == "$":
                    text = "R"
                elif line[index] == "#":
                    text = "M"
                else:
                    text = line[index]
                index += 1
                if index < len(line):
                    while line[index] not in (" ", "[", "]", "&", "%", "#", "$", "."): # will fail if incorrect spacing in code
                        text += line[index]
                        index += 1
                        if index >= len(line):
                            break
                try:
                    text = str(int(text, 0))
                except Exception:
                    pass
                if text.startswith("-"):
                    num = 0 - int(text[1: ], 0)
                    while num < 0:
                        num += (2 ** BITS)
                    text = str(num)
                elif (text.startswith("&")) and (bitOperator == "=="):
                    if text == "&BITS":
                        text = str(BITS)
                    elif text == "&MSB":
                        text = str(2 ** (BITS - 1))
                    elif text == "&SMSB":
                        text = str(2 ** (BITS - 2))
                    elif text == "&MAX":
                        text = str((2 ** BITS) - 1)
                    elif text == "&SMAX":
                        text = str((2 ** (BITS - 1)) - 1)
                    elif text == "&UHALF":
                        text = str(((2 ** (BITS // 2)) - 1) << (BITS // 2))
                    elif text == "&LHALF":
                        text = str((2 ** (BITS // 2)) - 1) # doesn't work for odd numbers of bits
                if text == "R0":
                    token.append("0")
                else:
                    token.append(text)
            elif line[index] in ("[", "]"):
                token.append(line[index])
                index += 1
            elif line[index] == " ":
                index += 1
            else:
                raise Exception(f"FATAL - Unrecognised symbol: {line[index]}")
        tokens.append(token)
    
    return tokens, headers
