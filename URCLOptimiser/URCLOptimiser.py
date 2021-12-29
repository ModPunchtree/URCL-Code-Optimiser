
# input MINREG, BITS, list of tokens

# clean code
    # convert relatives to labels
    # delete duplicate labels
    # move DW values to the end of the program

# label/branching optimisations
    # 1 delete duplicate labels
    # 2 shortcut branches
    # 3 delete useless branches

# constant folding

# single instruction optimisations
    #  1 ADD   -> LSH MOV INC DEC NOP
    #  2 RSH   -> MOV NOP
    #  3 LOD   -> NOP
    #  4 STR   -> 
    #  5 BGE   -> JMP BRZ BNZ BRN BRP NOP
    #  6 NOR   -> NOT MOV NOP
    #  7 SUB   -> MOV IMM NEG DEC INC NOP
    #  8 JMP   -> 
    #  9 MOV   -> IMM NOP
    # 10 NOP   -> delete
    # 11 IMM   -> NOP
    # 12 LSH   -> NOP
    # 13 INC   -> IMM NOP
    # 14 DEC   -> IMM NOP
    # 15 NEG   -> NOP
    # 16 AND   -> MOV IMM NOP
    # 17 OR    -> MOV IMM NOP
    # 18 NOT   -> IMM NOP
    # 19 XNOR  -> MOV IMM NOT NOP
    # 20 XOR   -> MOV IMM NOT NOP
    # 21 NAND  -> NOT IMM MOV NOP
    # 22 BRL   -> JMP BRZ BNZ BRN BRP NOP
    # 23 BRG   -> JMP BRZ BNZ BRN BRP NOP
    # 24 BRE   -> JMP BRZ NOP
    # 25 BNE   -> JMP BRZ NOP
    # 26 BOD   -> JMP NOP
    # 27 BEV   -> JMP NOP
    # 28 BLE   -> JMP BRZ BNZ NOP
    # 29 BRZ   -> JMP NOP
    # 30 BNZ   -> JMP NOP
    # 31 BRN   -> JMP NOP
    # 32 BRP   -> JMP NOP
    # 33 PSH   -> 
    # 34 POP   -> INC
    # 35 CAL   -> 
    # 36 RET   -> 
    # 37 HLT   -> 
    # 38 CPY   -> NOP
    # 39 BRC   -> JMP BNZ NOP
    # 40 BNC   -> JMP BRZ NOP
    
    # 41 MLT   -> LSH BSL MOV NOP
    # 42 DIV   -> RSH BSR MOV IMM NOP
    # 43 MOD   -> AND IMM NOP
    # 44 BSR   -> RSH MOV NOP
    # 45 BSL   -> LSH MOV NOP
    # 46 SRS   -> NOP
    # 47 BSS   -> SRS BSR MOV NOP
    # 48 SETE  -> IMM NOP
    # 49 SETNE -> IMM NOP
    # 50 SETG  -> IMM NOP
    # 51 SETL  -> IMM NOP
    # 52 SETGE -> IMM NOP
    # 53 SETLE -> IMM NOP
    # 54 SETC  -> IMM NOP
    # 55 SETNC -> IMM NOP
    # 56 LLOD  -> LOD NOP
    # 57 LSTR  -> STR
    
    # 58 IN    -> NOP
    # 59 OUT   -> 

# projectImmediates (send values from IMM instructions forward)

# pair optimisations
    # SETBRANCH
    # LODSTR
    # STRLOD
    # PSHPOP
    # POPPSH
    
    # ADDADD
    # SUBSUB
    # INCINC
    # DECDEC
    # ADDSUB
    # ADDINC
    # ADDDEC
    # SUBINC
    # SUBDEC
    # INCDEC
    # SUBADD
    # INCADD
    # DECADD
    # INCSUB
    # DECSUB
    # DECINC
    
    # MLTMLT
    # DIVDIV
    
    # LSHLSH
    # RSHRSH
    # SRSSRS
    # BSLBSL
    # BSRBSR
    # BSSBSS
    
    # LSHBSL
    # BSLLSH
    # RSHBSR
    # BSRRSH
    # SRSBSS
    # BSSSRS
    
    # simplify
    # RSHSRS
    # RSHBSS
    
    # bitmasks
    # LSHRSH
    # RSHLSH
    # LSHBSR
    # BSRLSH
    # RSHBSL
    # BSLRSH
    # BSLBSR
    # BSRBSL
    
    # ANDAND
    
    # XORXOR

# optimisation by emulation
    # only for short sections of code with no LOD STR LLOD LSTR PSH POP CAL RET HLT JMP BRANCH IN OUT

######################################################################################################
######################################################################################################
######################################################################################################

def convertRelativesToLabels(tokens: list[list[str]], uniqueNumber: int = 0) -> list[list[str]]:
    """
    Takes sanitised, tokenised URCL code and optionally a unique number for the label name.
    
    Returns URCL code with all relatives converted into labels. 
    """
    
    for index in range(len(tokens)):
        line = tokens[index]
        for tokenIndex, token in enumerate(line):
            if token.startswith("~"):
                relative = token
                number = int(relative[2: ], 0)
                if relative[1] == "+":
                    while number > 0:
                        index += 1
                        while tokens[index][0].startswith("."):
                            index += 1
                        number -= 1
                    tokens.insert(index, [f".__relative__{uniqueNumber}"])
                else:
                    while (number + 1) > 0:
                        index -= 1
                        while tokens[index][0].startswith("."):
                            index -= 1
                        number -= 1
                    tokens.insert(index, [f".__relative__{uniqueNumber}"])
                line[tokenIndex] = f".__relative__{uniqueNumber}"
                uniqueNumber += 1
                return convertRelativesToLabels(tokens, uniqueNumber)
    return tokens

def deleteDuplicateLabels(tokens: list[list[str]]) -> list[list[str]]:
    """
    Takes sanitised, tokenised URCL code.
    
    Returns URCL code with all duplicated labels removed.
    """

    index = 0
    while index < len(tokens) - 1:
        line = tokens[index]
        line2 = tokens[index + 1]
        if line[0].startswith(".") and line2[0].startswith("."):
            label = line[0]
            label2 = line2[0]
            for index3 in range(len(tokens)):
                line3 = tokens[index3]
                while line3.count(label2) != 0:
                    tokens[index3][line3.index(label2)] = label
            tokens.pop(index + 1)
        else:
            index += 1
    
    return tokens

def moveDWValues(tokens: list[list[str]]) -> list[list[str]]:
    """
    Takes sanitised, tokenised URCL code.
    
    Returns URCL code with all DW values moved to the end.
    """
    
    DWValues = []
    
    index = 0
    while index < len(tokens):
        line = tokens[index]
        if line[0] == "DW":
            DWValues.append(line)
            tokens.pop(index)
        elif line[0].startswith("."):
            if index < len(tokens) - 1:
                if tokens[index + 1][0] == "DW":
                    DWValues.append(line)
                    tokens.pop(index)
                else:
                    index += 1
            else:
                index += 1
        else:
            index += 1
    
    tokens += DWValues
    
    return tokens

def recursiveOptimisations(tokens: list[list[str]], BITS: int) -> list[list[str]]:
    """
    Takes sanitised, tokenised URCL code and the word length BITS.
    
    Tries to return URCL code with an optimisation applied, otherwise returns unoptimised code.
    """
    
    def shortcutBranches(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with branches that go to JMP shortcutted.
        """
        
        for index, line in enumerate(tokens):
            if line[0] in ("JMP", "BGE", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "CAL", "BRC", "BNC"):
                if line[1].startswith("."):
                    label = line[1]
                    for index2, line2 in enumerate(tokens):
                        if line2[0] == label:
                            if tokens[index2 + 1][0] == "JMP":
                                label2 = tokens[index2 + 1][1]
                                tokens[index][1] = label2
        
        return tokens
    
    def deleteUselessBranches(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with all of the branches that go to the next line, removed.
        """
        
        index = 0
        while index < len(tokens) - 1:
            line = tokens[index]
            if line[0] in ("JMP", "BGE", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "BRC", "BNC"):
                label = line[1]
                line2 = tokens[index + 1]
                if line2[0] == label:
                    tokens.pop(index)
                else:
                    index += 1
            else:
                index += 1
        
        return tokens
    
    def deleteUselessLabels(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with all unreferenced labels removed.
        """
        
        index = 0
        while index < len(tokens):
            line = tokens[index]
            if line[0].startswith("."):
                label = line[0]
                useless = True
                for line2 in tokens:
                    if (line2.count(label) > 0) and (len(line2) > 1):
                        useless = False
                        break
                if useless:
                    tokens.pop(index)
                else:
                    index += 1
            else:
                index += 1
        
        return tokens
    
    def deleteUnreachableCode(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with all unreachable lines removed.
        """
        
        index = 0
        while index < len(tokens) - 1:
            line = tokens[index]
            if line[0] in ("HLT", "RET", "JMP"):
                line2 = tokens[index + 1]
                if not(line2[0].startswith(".")):
                    tokens.pop(index + 1)
                else:
                    index += 1
            else:
                index += 1
        
        return tokens
    
    def constantFold(tokens: list[list[str]], BITS: int) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with instructions constant folded where possible.
        """
        
        def correctValue(value: int, BITS: int) -> int:
            """
            Takes a value and simulates roll over using a word length specified by BITS.
            
            Returns the value corrected so that it fits in the stated word length.
            """
            
            while value < 0:
                value += (2 ** BITS)
            value %= (2 ** BITS)
            
            return value
        
        # constant folding
        index = 0
        while index < len(tokens):
            line = tokens[index]
            op = line[0]
            if len(line) > 1:
                ops = line[1: ]
            
            #  1 ADD   -> LSH MOV INC DEC NOP
            if op == "ADD":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) + int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            #  2 RSH   -> MOV NOP
            elif op == "RSH":
                if ops[1].isnumeric():
                    number = int(ops[1]) >> 1
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            #  3 LOD   -> NOP
            elif op == "LOD":
                index += 1
            
            #  4 STR   -> 
            elif op == "STR":
                index += 1
            
            #  5 BGE   -> JMP BRZ BNZ BRN BRP NOP
            elif op == "BGE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = int(ops[1]) >= int(ops[2])
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            #  6 NOR   -> NOT MOV NOP
            elif op == "NOR":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = ((2 ** BITS) - 1) - (int(ops[1]) | int(ops[2]))
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            #  7 SUB   -> MOV IMM NEG DEC INC NOP
            elif op == "SUB":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) - int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            #  8 JMP   -> 
            elif op == "JMP":
                index += 1
            
            #  9 MOV   -> IMM NOP
            elif op == "MOV":
                index += 1
            
            # 10 NOP   -> delete
            elif op == "NOP":
                tokens.pop(index)
            
            # 11 IMM   -> NOP
            elif op == "IMM":
                index += 1
            
            # 12 LSH   -> NOP
            elif op == "LSH":
                if ops[1].isnumeric():
                    number = int(ops[1]) << 1
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 13 INC   -> IMM NOP
            elif op == "INC":
                if ops[1].isnumeric():
                    number = int(ops[1]) + 1
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 14 DEC   -> IMM NOP
            elif op == "DEC":
                if ops[1].isnumeric():
                    number = int(ops[1]) - 1
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 15 NEG   -> NOP
            elif op == "NEG":
                if ops[1].isnumeric():
                    number = 0 - int(ops[1])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 16 AND   -> MOV IMM NOP
            elif op == "AND":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) & int(ops[2])
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 17 OR    -> MOV IMM NOP
            elif op == "OR":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) | int(ops[2])
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 18 NOT   -> IMM NOP
            elif op == "NOT":
                if ops[1].isnumeric():
                    number = 0 - int(ops[1]) - 1
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 19 XNOR  -> MOV IMM NOT NOP
            elif op == "XNOR":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = 0 - (int(ops[1]) ^ int(ops[2])) - 1
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 20 XOR   -> MOV IMM NOT NOP
            elif op == "XOR":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) ^ int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 21 NAND  -> NOT IMM MOV NOP
            elif op == "NAND":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = 0 - (int(ops[1]) & int(ops[2])) - 1
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 22 BRL   -> JMP BRZ BNZ BRN BRP NOP
            elif op == "BRL":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = int(ops[1]) < int(ops[2])
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 23 BRG   -> JMP BRZ BNZ BRN BRP NOP
            elif op == "BRG":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = int(ops[1]) > int(ops[2])
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 24 BRE   -> JMP BRZ NOP
            elif op == "BRE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = int(ops[1]) == int(ops[2])
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 25 BNE   -> JMP BRZ NOP
            elif op == "BNE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = int(ops[1]) != int(ops[2])
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 26 BOD   -> JMP NOP
            elif op == "BOD":
                if ops[1].isnumeric():
                    condition = int(ops[1]) % 2
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 27 BEV   -> JMP NOP
            elif op == "BEV":
                if ops[1].isnumeric():
                    condition = int(ops[1]) % 2
                    if not(condition):
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 28 BLE   -> JMP BRZ BNZ NOP
            elif op == "BLE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = int(ops[1]) <= int(ops[2])
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 29 BRZ   -> JMP NOP
            elif op == "BRZ":
                if ops[1].isnumeric():
                    condition = int(ops[1]) == 0
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 30 BNZ   -> JMP NOP
            elif op == "BNZ":
                if ops[1].isnumeric():
                    condition = int(ops[1]) != 0
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 31 BRN   -> JMP NOP
            elif op == "BRN":
                if ops[1].isnumeric():
                    condition = int(ops[1]) >= (2 ** (BITS - 1))
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 32 BRP   -> JMP NOP
            elif op == "BRP":
                if ops[1].isnumeric():
                    condition = int(ops[1]) < (2 ** (BITS - 1))
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 33 PSH   -> 
            elif op == "PSH":
                index += 1
            
            # 34 POP   -> INC
            elif op == "POP":
                index += 1
            
            # 35 CAL   -> 
            elif op == "CAL":
                index += 1
            
            # 36 RET   -> 
            elif op == "RET":
                index += 1
            
            # 37 HLT   -> 
            elif op == "HLT":
                index += 1
            
            # 38 CPY   -> NOP
            elif op == "CPY":
                index += 1
            
            # 39 BRC   -> JMP BNZ NOP
            elif op == "BRC":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = (int(ops[1]) + int(ops[2])) >= (2 ** BITS)
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # 40 BNC   -> JMP BRZ NOP
            elif op == "BNC":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    condition = (int(ops[1]) + int(ops[2])) < (2 ** BITS)
                    if condition:
                        tokens[index] = ["JMP", ops[0]]
                        index += 1
                    else:
                        tokens.pop(index)
                else:
                    index += 1
            
            # complex instructions
            # 41 MLT   -> LSH BSL MOV NOP
            elif op == "MLT":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) * int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 42 DIV   -> RSH BSR MOV IMM NOP
            elif op == "DIV":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) // int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 43 MOD   -> AND IMM NOP
            elif op == "MOD":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) % int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 44 BSR   -> RSH MOV NOP
            elif op == "BSR":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) >> int(ops[2])
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 45 BSL   -> LSH MOV NOP
            elif op == "BSL":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) << int(ops[2])
                    number = correctValue(number, BITS)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 46 SRS   -> NOP
            elif op == "SRS":
                if ops[1].isnumeric():
                    number = int(ops[1])
                    if number >= (2 ** (BITS - 1)):
                        number >>= 1
                        number += (2 ** (BITS - 1))
                    else:
                        number >>= 1
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 47 BSS   -> SRS BSR MOV NOP
            elif op == "BSS":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1])
                    number2 = int(ops[2])
                    while number2 > 0:
                        if number >= (2 ** (BITS - 1)):
                            number >>= 1
                            number += (2 ** (BITS - 1))
                        else:
                            number >>= 1
                        number2 -= 1
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 48 SETE  -> IMM NOP
            elif op == "SETE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(int(ops[1]) == int(ops[2])) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 49 SETNE -> IMM NOP
            elif op == "SETNE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(int(ops[1]) != int(ops[2])) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 50 SETG  -> IMM NOP
            elif op == "SETG":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(int(ops[1]) > int(ops[2])) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 51 SETL  -> IMM NOP
            elif op == "SETL":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(int(ops[1]) < int(ops[2])) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 52 SETGE -> IMM NOP
            elif op == "SETGE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(int(ops[1]) >= int(ops[2])) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 53 SETLE -> IMM NOP
            elif op == "SETLE":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(int(ops[1]) <= int(ops[2])) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 54 SETC  -> IMM NOP
            elif op == "SETC":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int((int(ops[1]) + int(ops[2])) >= (2 ** BITS)) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 55 SETNC -> IMM NOP
            elif op == "SETNC":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int((int(ops[1]) + int(ops[2])) < (2 ** BITS)) * ((2 ** BITS) - 1)
                    tokens[index] = ["IMM", ops[0], str(number)]
                index += 1
            
            # 56 LLOD  -> LOD NOP
            elif op == "LLOD":
                if ops[1].isnumeric() and ops[2].isnumeric():
                    number = int(ops[1]) + int(ops[2])
                    tokens[index] = ["LOD", ops[0], str(number)]
                index += 1
            
            # 57 LSTR  -> STR
            elif op == "LSTR":
                if ops[0].isnumeric() and ops[1].isnumeric():
                    number = int(ops[0]) + int(ops[1])
                    tokens[index] = ["STR", str(number), ops[2]]
                index += 1
            
            # I/O instructions
            # 58 IN    -> NOP
            elif op == "IN":
                index += 1
            
            # 59 OUT   -> 
            elif op == "OUT":
                index += 1
            
            elif (op.startswith(".")) or (op == "DW"):
                index += 1
            else:
                raise Exception(f"FATAL - Unrecognised instruction operand: {op}")
        
        return tokens
    
    
    
    # label/branching optimisations
    # 1 shortcut branches
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = shortcutBranches(tokens)
    if oldTokens != tokens:
        return tokens

    # 2 delete useless branches
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = deleteUselessBranches(tokens)
    if oldTokens != tokens:
        return tokens
    
    # redelete duplicate labels
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = deleteDuplicateLabels(tokens)
    if oldTokens != tokens:
        return tokens
    
    # 3 delete useless labels
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = deleteUselessLabels(tokens)
    if oldTokens != tokens:
        return tokens
    
    # 4 delete unreachable code
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = deleteUnreachableCode(tokens)
    if oldTokens != tokens:
        return tokens

    # constant folding
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = constantFold(tokens, BITS)
    if oldTokens != tokens:
        return tokens



# projectImmediates (send values from IMM instructions forward)

# pair optimisations
    # SETBRANCH
    # LODSTR
    # STRLOD
    # PSHPOP
    # POPPSH
    
    # ADDADD
    # SUBSUB
    # INCINC
    # DECDEC
    # ADDSUB
    # ADDINC
    # ADDDEC
    # SUBINC
    # SUBDEC
    # INCDEC
    # SUBADD
    # INCADD
    # DECADD
    # INCSUB
    # DECSUB
    # DECINC
    
    # MLTMLT
    # DIVDIV
    
    # LSHLSH
    # RSHRSH
    # SRSSRS
    # BSLBSL
    # BSRBSR
    # BSSBSS
    
    # LSHBSL
    # BSLLSH
    # RSHBSR
    # BSRRSH
    # SRSBSS
    # BSSSRS
    
    # simplify
    # RSHSRS
    # RSHBSS
    
    # bitmasks
    # LSHRSH
    # RSHLSH
    # LSHBSR
    # BSRLSH
    # RSHBSL
    # BSLRSH
    # BSLBSR
    # BSRBSL
    
    # ANDAND
    
    # XORXOR

# optimisation by emulation
    # only for short sections of code with no LOD STR LLOD LSTR PSH POP CAL RET HLT JMP BRANCH IN OUT
    
    return tokens

# input MINREG, BITS, list of tokens
def URCLOptimiser(tokens: list[list[str]], rawHeaders: tuple[int, str, int, int, int, str]) -> tuple[list[list[str]], tuple[int, str, int, int, int, str]]:
    """
    Takes sanitised, tokenised URCL code.
    
    Returns optimised URCL code and optimised headers.
    """

    # clean code
    # convert relatives to labels
    tokens = convertRelativesToLabels(tokens)
    
    # delete duplicate labels
    tokens = deleteDuplicateLabels(tokens)
    
    # move DW values to the end of the program
    tokens = moveDWValues(tokens)

    # recursive optimisations
    oldTokens = []
    while tokens != oldTokens:
        oldTokens = [([token for token in line]) for line in tokens]
        tokens = recursiveOptimisations(tokens, rawHeaders[0])

    # calculate optimsied headers
    #####################################################

    return tokens, rawHeaders
