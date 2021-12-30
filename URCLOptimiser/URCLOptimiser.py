
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
    
    def projectImmediates(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with values from IMM instructions projected forwards.
        """
        
        for index, line in enumerate(tokens):
            if line[0] == "IMM":
                if line[1] != "0":
                    register = line[1]
                    immediate = line[2]
                    for index2, line2 in enumerate(tokens[index + 1: ]):
                        if line2[0] in ("LOD", "STR", "BGE", "JMP", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "PSH", "CAL", "CPY", "BRC", "BNC", "LLOD", "LSTR", "OUT"):
                            if line2[1] == register: # read from op1
                                tokens[index + 1 + index2][1] = immediate
                        if line2[0] in ("ADD", "RSH", "LOD", "STR", "BGE", "NOR", "SUB", "MOV", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "CPY", "BRC", "BNC", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "LLOD", "LSTR", "IN", "OUT"):
                            if line2[2] == register: # read from op2
                                tokens[index + 1 + index2][2] = immediate
                        if line2[0] in ("ADD", "BGE", "NOR", "SUB", "AND", "OR", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BLE", "BRC", "BNC", "MLT", "DIV", "MOD", "BSR", "BSL", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "LLOD", "LSTR"):
                            if line2[3] == register: # read from op3
                                tokens[index + 1 + index2][3] = immediate
                        if line2[0] in ("ADD", "RSH", "NOR", "SUB", "MOV", "IMM", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "POP", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "IN"):
                            if line2[1] == register: # write to op1
                                break
                        if (line2[0].startswith(".")) or (line2[0] in ("JMP", "HLT", "RET")):
                            break # label or JMP, RET, HLT
        
        return tokens
    
    def writeBeforeRead(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with all instructions whoes output is overwritten before being read, removed.
        """
        
        index = 0
        while index < len(tokens):
            line = tokens[index]
            useless = False
            if line[0] in ("ADD", "RSH", "NOR", "SUB", "MOV", "IMM", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "POP", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "IN"):
                register = line[1]
                useless = True
                for line2 in tokens[index + 1: ]:
                    if line2[0] in ("LOD", "STR", "BGE", "JMP", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "PSH", "CAL", "CPY", "BRC", "BNC", "LLOD", "LSTR", "OUT"):
                        if line2[1] == register: # reads from op1
                            useless = False
                            break
                    if line2[0] in ("ADD", "RSH", "LOD", "STR", "BGE", "NOR", "SUB", "MOV", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "CPY", "BRC", "BNC", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "LLOD", "LSTR", "IN", "OUT"):
                        if line2[2] == register: # reads from op2
                            useless = False
                            break
                    if line2[0] in ("ADD", "BGE", "NOR", "SUB", "AND", "OR", "XNOR", "XOR", "NAND", "BRL", "BRG", "BRE", "BNE", "BLE", "BRC", "BNC", "MLT", "DIV", "MOD", "BSR", "BSL", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "LLOD", "LSTR"):
                        if line2[3] == register: # reads from op3
                            useless = False
                            break
                    if line2[0] in ("ADD", "RSH", "NOR", "SUB", "MOV", "IMM", "LSH", "INC", "DEC", "NEG", "AND", "OR", "NOT", "XNOR", "XOR", "NAND", "POP", "MLT", "DIV", "MOD", "BSR", "BSL", "SRS", "BSS", "SETE", "SETNE", "SETG", "SETL", "SETGE", "SETLE", "SETC", "SETNC", "IN"):
                        if line2[1] == register: # writes to op1
                            break
                    if line2[0] in ("BGE", "BRL", "BRG", "BRE", "BNE", "BOD", "BEV", "BLE", "BRZ", "BNZ", "BRN", "BRP", "CAL", "HLT", "BRC", "BNC"):
                        break # branch or HLT
            if useless:
                tokens.pop(index)
            else:
                index += 1
        
        return tokens
    
    def SETBranch(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with BRZ and BNZ optimised if they are preceded by a SET instruction.
        """
        
        for index in range(len(tokens) - 1):
            line = tokens[index]
            if line[0].startswith("SET"):
                register = line[1]
                line2 = tokens[index + 1]
                if line2[0] == "BRZ":
                    if register == line2[2]:
                        if line[0] == "SETE":
                            tokens[index + 1] = ["BNE", line[1], line[2], line[3]]
                        elif line[0] == "SETNE":
                            tokens[index + 1] = ["BRE", line[1], line[2], line[3]]
                        elif line[0] == "SETG":
                            tokens[index + 1] = ["BLE", line[1], line[2], line[3]]
                        elif line[0] == "SETL":
                            tokens[index + 1] = ["BGE", line[1], line[2], line[3]]
                        elif line[0] == "SETGE":
                            tokens[index + 1] = ["BRL", line[1], line[2], line[3]]
                        elif line[0] == "SETLE":
                            tokens[index + 1] = ["BRG", line[1], line[2], line[3]]
                        elif line[0] == "SETC":
                            tokens[index + 1] = ["BNC", line[1], line[2], line[3]]
                        elif line[0] == "SETNC":
                            tokens[index + 1] = ["BRC", line[1], line[2], line[3]]
                if line2[0] == "BNZ":
                    if register == line2[2]:
                        if line[0] == "SETE":
                            tokens[index + 1] = ["BRE", line[1], line[2], line[3]]
                        elif line[0] == "SETNE":
                            tokens[index + 1] = ["BNE", line[1], line[2], line[3]]
                        elif line[0] == "SETG":
                            tokens[index + 1] = ["BRG", line[1], line[2], line[3]]
                        elif line[0] == "SETL":
                            tokens[index + 1] = ["BRL", line[1], line[2], line[3]]
                        elif line[0] == "SETGE":
                            tokens[index + 1] = ["BGE", line[1], line[2], line[3]]
                        elif line[0] == "SETLE":
                            tokens[index + 1] = ["BLE", line[1], line[2], line[3]]
                        elif line[0] == "SETC":
                            tokens[index + 1] = ["BRC", line[1], line[2], line[3]]
                        elif line[0] == "SETNC":
                            tokens[index + 1] = ["BNC", line[1], line[2], line[3]]

        return tokens
    
    def LODSTR(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with LOD followed by STR to the same location optimised.
        """
        
        index = 0
        while index < len(tokens) - 1:
            line = tokens[index]
            line2 = tokens[index + 1]
            if (line[0] == "LOD") and (line2[0] == "STR"):
                if (line[2] == line2[0]) and (line[1] != line[2]):
                    tokens.pop(index + 1)
            index += 1
        
        return tokens
    
    def STRLOD(tokens: list[list[str]]) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with STR followed by LOD to the same location optimised.
        """
        
        index = 0
        while index < len(tokens) - 1:
            line = tokens[index]
            line2 = tokens[index + 1]
            if (line[0] == "STR") and (line2[0] == "LOD"):
                if line[1] == line2[2]:
                    if line[2] == line2[1]:
                        tokens.pop(index + 1)
                    else:
                        tokens[index + 1] = ["MOV", line2[1], line[2]]
                    tokens.pop(index + 1)
            index += 1
        
        return tokens
    
    def singleInstructionOptimisations(tokens: list[list[str]], BITS: int) -> list[list[str]]:
        """
        Takes sanitised, tokenised URCL code.
        
        Returns URCL code with each instruction optimised independently of all other instructions.
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
        
        index = 0
        while index < len(tokens):
            line = tokens[index]
            op = line[0]
            if len(line) > 1:
                ops = line[1: ]
            
            #  1 ADD   -> LSH MOV INC DEC NOP
            if op == "ADD":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["LSH", ops[0], ops[1]]
                    index += 1
                elif ops[1] == "1":
                    tokens[index] = ["INC", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "1":
                    tokens[index] = ["INC", ops[0], ops[1]]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["DEC", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["DEC", ops[0], ops[1]]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["MOV", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            #  2 RSH   -> MOV NOP
            elif op == "RSH":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            #  3 LOD   -> NOP
            elif op == "LOD":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            #  4 STR   -> 
            elif op == "STR":
                index += 1
            
            #  5 BGE   -> JMP BRZ BRN BRP
            elif op == "BGE":
                if ops[2] == "0":
                    tokens[index] = ["JMP", ops[0]]
                elif ops[1] == ops[2]:
                    tokens[index] = ["JMP", ops[0]]
                elif ops[2] == (2 ** (BITS - 1)):
                    tokens[index] = ["BRN", ops[0], ops[1]]
                elif ops[1] == ((2 ** (BITS - 1)) - 1):
                    tokens[index] = ["BRP", ops[0], ops[2]]
                elif ops[1] == "0":
                    tokens[index] = ["BRZ", ops[0], ops[2]]
                index += 1
            
            #  6 NOR   -> NOT MOV NOP
            elif op == "NOR":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["NOT", ops[0], ops[2]]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["NOT", ops[0], ops[2]]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["NOT", ops[0], ops[1]]
                    index += 1
                elif ops[1] == str(((2 ** BITS) - 1)):
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2] == str(((2 ** BITS) - 1)):
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                else:
                    index += 1
            
            #  7 SUB   -> MOV IMM NEG DEC INC NOP
            elif op == "SUB":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["NEG", ops[0], ops[2]]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["NOT", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[2] == "1":
                    tokens[index] = ["DEC", ops[0], ops[1]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["INC", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            #  8 JMP   -> 
            elif op == "JMP":
                index += 1
            
            #  9 MOV   -> IMM NOP
            elif op == "MOV":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1].isnumeric():
                    tokens[index][0] = "IMM"
                    index += 1
                else:
                    index += 1
            
            # 10 NOP   -> delete
            elif op == "NOP":
                tokens.pop(index)
            
            # 11 IMM   -> NOP
            elif op == "IMM":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 12 LSH   -> NOP
            elif op == "LSH":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 13 INC   -> NOP
            elif op == "INC":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 14 DEC   -> NOP
            elif op == "DEC":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 15 NEG   -> NOP
            elif op == "NEG":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 16 AND   -> MOV IMM NOP
            elif op == "AND":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["MOV", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 17 OR    -> MOV IMM NOP
            elif op == "OR":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["MOV", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                else:
                    index += 1
            
            # 18 NOT   -> NOP
            elif op == "NOT":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 19 XNOR  -> MOV IMM NOT NOP
            elif op == "XNOR":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["NOT", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["NOT", ops[0], ops[1]]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["MOV", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 20 XOR   -> MOV IMM NOT NOP
            elif op == "XOR":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["MOV", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["NOT", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["NOT", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 21 NAND  -> NOT IMM NOP
            elif op == "NAND":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["NOT", ops[0], ops[1]]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["NOT", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["NOT", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 22 BRL   -> BRZ BNZ BRN BRP NOP
            elif op == "BRL":
                if ops[1] == "0":
                    tokens[index] = ["BNZ", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens.pop(index)
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens.pop(index)
                elif ops[2] == "1":
                    tokens[index] = ["BRZ", ops[0], ops[1]]
                    index += 1
                elif ops[2] == str(2 ** (BITS - 1)):
                    tokens[index] = ["BRP", ops[0], ops[1]]
                    index += 1
                elif ops[1] == str((2 ** (BITS - 1)) - 1):
                    tokens[index] = ["BRN", ops[0], ops[2]]
                    index += 1
                else:
                    index += 1
            
            # 23 BRG   -> BRZ BNZ BRN BRP NOP
            elif op == "BRG":
                if ops[2] == "0":
                    tokens[index] = ["BNZ", ops[0], ops[2]]
                    index += 1
                elif ops[1] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens.pop(index)
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens.pop(index)
                elif ops[1] == "1":
                    tokens[index] = ["BRZ", ops[0], ops[2]]
                    index += 1
                elif ops[1] == str(2 ** (BITS - 1)):
                    tokens[index] = ["BRP", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** (BITS - 1)) - 1):
                    tokens[index] = ["BRN", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 24 BRE   -> JMP BRZ
            elif op == "BRE":
                if ops[1] == ops[2]:
                    tokens[index] = ["JMP", ops[0]]
                elif ops[1] == "0":
                    tokens[index] = ["BRZ", ops[0], ops[2]]
                elif ops[2] == "0":
                    tokens[index] = ["BRZ", ops[0], ops[1]]
                index += 1
            
            # 25 BNE   -> BRZ NOP
            elif op == "BNE":
                if ops[1] == ops[2]:
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["BNZ", ops[0], ops[2]]
                elif ops[2] == "0":
                    tokens[index] = ["BNZ", ops[0], ops[1]]
                else:
                    index += 1
            
            # 26 BOD   -> JMP NOP
            elif op == "BOD":
                index += 1
            
            # 27 BEV   -> JMP NOP
            elif op == "BEV":
                index += 1
            
            # 28 BLE   -> JMP BRP BRN BRZ
            elif op == "BLE":
                if ops[1] == ops[2]:
                    tokens[index] = ["JMP", ops[0]]
                elif ops[1] == "0":
                    tokens[index] = ["JMP", ops[0]]
                elif ops[2] == "0":
                    tokens[index] = ["BRZ", ops[0], ops[1]]
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["JMP", ops[0]]
                elif ops[2] == str((2 ** (BITS - 1)) - 1):
                    tokens[index] = ["BRP", ops[0], ops[1]]
                elif ops[1] == str(2 ** (BITS - 1)):
                    tokens[index] = ["BRN", ops[0], ops[2]]
                index += 1
            
            # 29 BRZ   ->
            elif op == "BRZ":
                index += 1
            
            # 30 BNZ   ->
            elif op == "BNZ":
                index += 1
            
            # 31 BRN   ->
            elif op == "BRN":
                index += 1
            
            # 32 BRP   ->
            elif op == "BRP":
                index += 1
            
            # 33 PSH   -> 
            elif op == "PSH":
                index += 1
            
            # 34 POP   -> INC
            elif op == "POP":
                if ops[0] == "0":
                    tokens[index] == ["INC", "SP", "SP"]
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
                if ops[1] == ops[2]:
                    tokens.pop(index)
                else:
                    index += 1
            
            # 39 BRC   -> BNZ NOP
            elif op == "BRC":
                if ops[1] == "0":
                    tokens.pop(index)
                elif ops[2] == "0":
                    tokens.pop(index)
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["BNZ", ops[0], ops[2]]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["BNZ", ops[0], ops[1]]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["BRN", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 40 BNC   -> JMP BRZ
            elif op == "BNC":
                if ops[1] == "0":
                    tokens[index] = ["JMP", ops[0]]
                elif ops[2] == "0":
                    tokens[index] = ["JMP", ops[0]]
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["BRZ", ops[0], ops[2]]
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["BRZ", ops[0], ops[1]]
                elif ops[1] == ops[2]:
                    tokens[index] = ["BRP", ops[0], ops[1]]
                    index += 1
                index += 1
            
            # complex instructions
            # 41 MLT   -> LSH BSL MOV NOP
            elif op == "MLT":
                if ops[0] == "0":
                    tokens.pop(index)
                    index -= 1
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                elif ops[2] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                elif ops[1] == "1":
                    tokens[index] = ["MOV", ops[0], ops[2]]
                elif ops[2] == "1":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                elif ops[1] == "2":
                    tokens[index] = ["LSH", ops[0], ops[2]]
                elif ops[2] == "2":
                    tokens[index] = ["LSH", ops[0], ops[1]]
                else:
                    for number in range(BITS):
                        num = str(2 ** number)
                        if ops[1] == num:
                            tokens[index] = ["BSL", ops[0], ops[2], str(number)]
                            break
                        elif ops[2] == num:
                            tokens[index] = ["BSL", ops[0], ops[1], str(number)]
                            break
                index += 1 
            
            # 42 DIV   -> RSH BSR MOV IMM NOP
            elif op == "DIV":
                if ops[0] == "0":
                    tokens.pop(index)
                    index -= 1
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                elif ops[2] == "0":
                    raise Exception(f"FATAL - Division by zero: {line}")
                elif ops[2] == "1":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "1"]
                elif ops[2] == "2":
                    tokens[index] = ["RSH", ops[0], ops[1]]
                else:
                    for number in range(BITS):
                        num = str(2 ** number)
                        if ops[2] == num:
                            tokens[index] = ["BSR", ops[0], ops[1], str(number)]
                            break
                index += 1
            
            # 43 MOD   -> AND IMM NOP
            elif op == "MOD":
                if ops[0] == "0":
                    tokens.pop(index)
                    index -= 1
                elif ops[1] == "1":
                    tokens[index] = ["IMM", ops[0], "0"]
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                else:
                    for number in range(BITS):
                        num = str(2 ** number)
                        num2 = str((2 ** number) - 1)
                        if ops[2] == num:
                            tokens[index] = ["AND", ops[0], ops[1], num2]
                            break
                index += 1
            
            # 44 BSR   -> IMM RSH MOV NOP
            elif op == "BSR":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[2] == "1":
                    tokens[index] = ["RSH", ops[0], ops[1]]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2].isnumeric():
                    if int(ops[2]) >= BITS:
                        tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                else:
                    index += 1
            
            # 45 BSL   -> LSH MOV NOP
            elif op == "BSL":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[2] == "1":
                    tokens[index] = ["LSH", ops[0], ops[1]]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2].isnumeric():
                    if int(ops[2]) >= BITS:
                        tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                else:
                    index += 1
            
            # 46 SRS   -> NOP
            elif op == "SRS":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
                    index += 1
            
            # 47 BSS   -> SRS BSR MOV NOP
            elif op == "BSS":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[2] == "0":
                    tokens[index] = ["MOV", ops[0], ops[1]]
                    index += 1
                elif ops[2] == "1":
                    tokens[index] = ["SRS", ops[0], ops[1]]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[1].isnumeric():
                    if int(ops[1]) < str(2 ** (BITS - 1)):
                        tokens[index][0] = "BSR"
                    index += 1
                else:
                    index += 1
            
            # 48 SETE  -> IMM NOP
            elif op == "SETE":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                else:
                    index += 1
            
            # 49 SETNE -> IMM NOP
            elif op == "SETNE":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                else:
                    index += 1
            
            # 50 SETG  -> SETNE IMM NOP
            elif op == "SETG":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["SETNE", ops[0], ops[1], "0"]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                else:
                    index += 1
            
            # 51 SETL  -> SETNE IMM NOP
            elif op == "SETL":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == "0":
                    tokens[index] = ["SETNE", ops[0], ops[1], "0"]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                else:
                    index += 1
            
            # 52 SETGE -> SETE IMM NOP
            elif op == "SETGE":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[1] ==  "0":
                    tokens[index] = ["SETE", ops[0], ops[2], "0"]
                    index += 1
                elif ops[2] ==  "0":
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[1] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                else:
                    index += 1
            
            # 53 SETLE -> IMM NOP
            elif op == "SETLE":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == ops[2]:
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[2] ==  "0":
                    tokens[index] = ["SETE", ops[0], ops[1], "0"]
                    index += 1
                elif ops[1] ==  "0":
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                elif ops[2] == str((2 ** BITS) - 1):
                    tokens[index] = ["IMM", ops[0], str((2 ** BITS) - 1)]
                    index += 1
                else:
                    index += 1
            
            # 54 SETC  -> IMM NOP
            elif op == "SETC":
                if ops[0] == "0":
                    tokens.pop()
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["IMM", ops[0], "0"]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["SETGE", ops[0], str(2 ** (BITS - 1))]
                    index += 1
                elif ops[1].isnumeric():
                    tokens[index] = ["SETGE", ops[0], ops[2], str((2 ** BITS) - int(ops[1]))]
                    index += 1
                elif ops[2].isnumeric():
                    tokens[index] = ["SETGE", ops[0], ops[1], str((2 ** BITS) - int(ops[2]))]
                    index += 1
                else:
                    index += 1
            
            # 55 SETNC -> IMM NOP
            elif op == "SETNC":
                if ops[0] == "0":
                    tokens.pop()
                elif ops[1] == "0":
                    tokens[index] = ["IMM", ops[0], str(2 ** BITS)]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["IMM", ops[0], str(2 ** BITS)]
                    index += 1
                elif ops[1] == ops[2]:
                    tokens[index] = ["SETL", ops[0], str(2 ** (BITS - 1))]
                    index += 1
                elif ops[1].isnumeric():
                    tokens[index] = ["SETL", ops[0], ops[2], str((2 ** BITS) - int(ops[1]))]
                    index += 1
                elif ops[2].isnumeric():
                    tokens[index] = ["SETL", ops[0], ops[1], str((2 ** BITS) - int(ops[2]))]
                    index += 1
                else:
                    index += 1
            
            # 56 LLOD  -> LOD NOP
            elif op == "LLOD":
                if ops[0] == "0":
                    tokens.pop(index)
                elif ops[1] == "0":
                    tokens[index] = ["LOD", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["LOD", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # 57 LSTR  -> STR
            elif op == "LSTR":
                if ops[1] == "0":
                    tokens[index] = ["STR", ops[0], ops[2]]
                    index += 1
                elif ops[2] == "0":
                    tokens[index] = ["STR", ops[0], ops[1]]
                    index += 1
                else:
                    index += 1
            
            # I/O instructions
            # 58 IN    -> NOP
            elif op == "IN":
                if ops[0] == "0":
                    tokens.pop(index)
                else:
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

    # projectImmediates (send values from IMM instructions forwards)
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = projectImmediates(tokens)
    if oldTokens != tokens:
        return tokens

    # write before read
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = writeBeforeRead(tokens)
    if oldTokens != tokens:
        return tokens

    # single instruction optimisations
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = singleInstructionOptimisations(tokens, BITS)
    if oldTokens != tokens:
        return tokens

    # pair optimisations
    # SETBranch
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = SETBranch(tokens)
    if oldTokens != tokens:
        return tokens
    
    # LODSTR
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = LODSTR(tokens)
    if oldTokens != tokens:
        return tokens
    
    # STRLOD
    oldTokens = [([token for token in line]) for line in tokens]
    tokens = STRLOD(tokens)
    if oldTokens != tokens:
        return tokens
    
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