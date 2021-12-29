
# input MINREG, BITS, list of tokens

# clean code
    # 1 delete multiline comments
    # 2 delete line comments
    # 3 delete empty lines
    # 4 convert double spaces to single spaces, twice
    # 5 convert relatives to labels

# delete duplicate labels
# move DW values to the end of the program

# label/branching optimisations
    # 1 delete duplicate labels
    # 2 shortcut branches
    # 3 delete useless branches

# constant folding

# single instruction optimisations
    #  1 ADD
    #  2 RSH
    #  3 LOD
    #  4 STR
    #  5 BGE
    #  6 NOR
    #  7 SUB
    #  8 JMP
    #  9 MOV
    # 10 NOP
    # 11 IMM
    # 12 LSH
    # 13 INC
    # 14 DEC
    # 15 NEG
    # 16 AND
    # 17 OR
    # 18 NOT
    # 19 XNOR
    # 20 XOR
    # 21 NAND
    # 22 BRL
    # 23 BRG
    # 24 BRE
    # 25 BNE
    # 26 BOD
    # 27 BEV
    # 28 BLE
    # 29 BRZ
    # 30 BNZ
    # 31 BRN
    # 32 BRP
    # 33 PSH
    # 34 POP
    # 35 CAL
    # 36 RET
    # 37 HLT
    # 38 CPY
    # 39 BRC
    # 40 BNC
    
    # 41 MLT
    # 42 DIV
    # 43 MOD
    # 44 BSR
    # 45 BSL
    # 46 SRS
    # 47 BSS
    # 48 SETE
    # 49 SETNE
    # 50 SETG
    # 51 SETL
    # 52 SETGE
    # 53 SETLE
    # 54 SETC
    # 55 SETNC
    # 56 LLOD
    # 57 LSTR
    
    # 58 IN
    # 59 OUT
    
# single instruction optimisations
    # 1  ADD   -> LSH, MOV, INC, DEC, NOP
    # 2  RSH   -> MOV, NOP
    # 3  LOD   -> NOP
    # 4  STR   -> 
    # 5  JMP   -> 
    # 6  BGE   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 7  NOR   -> NOT, MOV, NOP
    # 8  SUB   -> MOV, NEG, DEC, INC, NOP
    # 9  MOV   -> IMM, NOP
    # 10 LSH   -> NOP
    # 11 DEC   -> NOP
    # 12 NEG   -> NOP
    # 13 AND   -> MOV, NOP
    # 14 OR    -> MOV, NOP
    # 15 NOT   -> MOV
    # 16 XNOR  -> XOR, NOT, MOV, NOP
    # 17 XOR   -> MOV, NOT, NOP
    # 18 NAND  -> NOT, MOV, NOP
    # 19 BRL   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 20 BRG   -> JMP, BRZ, BNZ, BRN, BRP, NOP
    # 21 BRE   -> JMP, BRZ, NOP
    # 22 BNE   -> JMP, BNZ, NOP
    # 23 BOD   -> JMP, NOP
    # 24 BEV   -> JMP, NOP
    # 25 BLE   -> JMP, BRZ, BNZ, NOP
    # 26 BRZ   -> JMP, NOP
    # 27 BNZ   -> JMP, NOP
    # 28 BRN   -> JMP, NOP
    # 29 BRP   -> JMP, NOP
    # 30 PSH   -> 
    # 31 POP   -> INC
    # 32 CAL   -> 
    # 33 RET   -> 
    # 34 HLT   -> 
    # 35 MLT   -> LSH, BSL, MOV, NOP
    # 36 DIV   -> RSH, BSR, MOV, NOP
    # 37 MOD   -> AND, MOV, NOP
    # 38 BSR   -> RSH, MOV, NOP
    # 39 BSL   -> LSH, MOV, NOP
    # 40 SRS   -> MOV, NOP
    # 41 BSS   -> SRS, BSR, MOV, NOP
    # 42 SETE  -> MOV, NOP
    # 43 SETNE -> MOV, NOP
    # 44 SETG  -> MOV, NOP
    # 45 SETL  -> MOV, NOP
    # 46 SETGE -> MOV, NOP
    # 47 SETLE -> MOV, NOP
    # 48 INC   -> MOV, NOP
    # 49 NOP   -> 
    # 50 IMM   -> NOP

# miscellaneous optimisations
    # SETBRANCH
    # LODSTR
    # STRLOD
    # PSHPOP
    # POPPSH

# optimisation by emulation
    # only for short sections of code with no LOD STR LLOD LSTR PSH POP CAL RET HLT JMP BRANCH IN OUT

