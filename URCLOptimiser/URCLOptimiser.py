
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
            tokens.pop(index + 1)
        else:
            index += 1
    
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

    return tokens, rawHeaders
