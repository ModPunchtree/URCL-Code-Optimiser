
from URCLOptimiser.URCLOptimiser import URCLOptimiser
from URCLTokeniser.URCLTokeniser import URCLTokeniser


tokens, rawHeaders = URCLTokeniser()

tokens, headers = URCLOptimiser(tokens, rawHeaders)

output = ""
for line in tokens:
    output += " ".join(line) + "\n"
output = output[: -1]

print(output)
#print(headers)
