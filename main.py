
from URCLOptimiser.URCLOptimiser import URCLOptimiser
from URCLTokeniser.URCLTokeniser import URCLTokeniser


tokens, rawHeaders = URCLTokeniser()

tokens, headers = URCLOptimiser(tokens, rawHeaders)

print(tokens)
print(headers)
