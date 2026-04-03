#!/usr/bin/env python3
"""
Patches all NotImplementedError stubs - v2: splits file into individual functions,
patches each independently, then reassembles.
"""
import re, json, sys, os

sys.stdout.reconfigure(encoding='utf-8')
BASE = 'C:/Users/ISR831/Documents/git/instltns'

with open(os.path.join(BASE, 'financial_functions_1.py'), 'r', encoding='utf-8') as f:
    content = f.read()

# Load implementations from patch_stubs.py by exec-ing just the IMPL dict
exec_globals = {}
exec_code = """
IMPL = {}
def impl(name, params, body):
    IMPL[name] = (params, body)
"""

# Read patch_stubs.py and extract all impl() calls
with open(os.path.join(BASE, 'patch_stubs.py'), 'r', encoding='utf-8') as f:
    patch_content = f.read()

# Extract everything between the first impl( and the APPLY PATCHES section
start = patch_content.find("impl('abnormal_earnings_growth'")
end = patch_content.find("# APPLY PATCHES")
impl_code = exec_code + patch_content[start:end]
exec(impl_code, exec_globals)
IMPL = exec_globals['IMPL']
print(f"Loaded {len(IMPL)} implementations")

# Split file into header and functions
# Find the first 'def ' line
lines = content.split('\n')
header_end = 0
for i, line in enumerate(lines):
    if line.startswith('def '):
        header_end = i
        break

header = '\n'.join(lines[:header_end])

# Split into individual functions
# Each function starts with 'def ' at column 0 and ends just before the next 'def '
func_blocks = []
current_start = header_end
for i in range(header_end + 1, len(lines)):
    if lines[i].startswith('def '):
        func_blocks.append('\n'.join(lines[current_start:i]))
        current_start = i
# Last function
func_blocks.append('\n'.join(lines[current_start:]))

print(f"Split into {len(func_blocks)} function blocks")

# Patch each function block that has NotImplementedError
patched_count = 0
new_blocks = []

for block in func_blocks:
    if 'raise NotImplementedError' not in block:
        new_blocks.append(block)
        continue

    # Extract function name
    m = re.match(r'def (\w+)\(', block)
    if not m:
        new_blocks.append(block)
        continue

    fname = m.group(1)
    if fname not in IMPL:
        new_blocks.append(block)
        continue

    new_params, new_body = IMPL[fname]

    # Split block into lines
    blines = block.split('\n')

    # Find docstring boundaries
    doc_start = None
    doc_end = None
    tq_count = 0
    for j, line in enumerate(blines):
        if line.strip() == "'''":
            tq_count += 1
            if tq_count == 1:
                doc_start = j
            elif tq_count == 2:
                doc_end = j
                break

    if doc_end is None:
        new_blocks.append(block)
        continue

    # Rebuild function:
    # 1. New def line with new params
    # 2. Docstring (unchanged)
    # 3. New body
    new_def_line = f'def {fname}({new_params}):'
    docstring_lines = blines[doc_start:doc_end + 1]

    rebuilt = [new_def_line] + docstring_lines + new_body.split('\n')
    new_blocks.append('\n'.join(rebuilt))
    patched_count += 1

print(f"Patched {patched_count} functions")

# Reassemble
output = header + '\n' + '\n\n\n'.join(new_blocks)

# Verify
try:
    compile(output, 'financial_functions_2.py', 'exec')
    print('Syntax: OK')
except SyntaxError as e:
    print(f'Syntax Error at line {e.lineno}: {e.msg}')
    olines = output.split('\n')
    for i in range(max(0, e.lineno-3), min(len(olines), e.lineno+3)):
        print(f'  {i+1}: {olines[i]!r}')

# Count
defs = re.findall(r'^def (\w+)\(', output, re.MULTILINE)
nie = len(re.findall(r'NotImplementedError', output))
print(f'Total functions: {len(defs)}')
print(f'NotImplementedError remaining: {nie}')
print(f'Lines: {output.count(chr(10))}')

# Write
out_path = os.path.join(BASE, 'financial_functions_2.py')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(output)
print(f'Written to {out_path}')
