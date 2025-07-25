import re
from pathlib import Path

# Grabs all directories needed to run scripts and log files.
root = Path(__file__).resolve().parent.parent
script_dir = root / "scripts"
src_dir = root / "src"
mem_src = src_dir / "program.mem"
assembly_src = script_dir / "Program.asm"

src_file = open(assembly_src, 'r')
mem_file = open(mem_src, 'w')

formats = {
    'ADD': {
        "format": ['rd', 'ra', 'rb'],
        "opcode": "0000"},
    'SUB': {
        "format": ['rd', 'ra', 'rb'],
        "opcode": "0001"},
    'AND': {
        "format": ['rd', 'ra', 'rb'],
        "opcode": "0010"},
    'OR': {
        "format": ['rd', 'ra', 'rb'],
        "opcode": "0011"},
    'XOR': {
        "format": ['rd', 'ra', 'rb'],
        "opcode": "0100"},
    'NOT': {
        "format": ['rd', 'ra'],
        "opcode": "0101"},
    'SHL': {
        "format": ['rd', 'ra'],
        "opcode": "0110"},
    'SHR': {
        "format": ['rd', 'ra'],
        "opcode": "0111"},
    'ADDI': {
        "format": ['rd', 'ra', 'imm'],
        "opcode": "1000"},
    'ANDI': {
        "format": ['rd', 'ra', 'imm'],
        "opcode": "1001"},
    'LOAD': {
        "format": ['rd', 'ra', 'imm'],
        "opcode": "1010"},
    'STORE': {
        "format": ['ra', 'rb', 'imm'],
        "opcode": "1011"},
    'BEQ': {
        "format": ['ra', 'rb', 'imm'],
        "opcode": "1100"},
    'BNE': {
        "format": ['ra', 'rb', 'imm'],
        "opcode": "1101"},
    'JMP': {
        "format": ['ra', 'imm'],
        "opcode": "1110"},
    'HALT': {
        "format": ['imm'],
        "opcode": "1111"}
}

def reg_to_bin(reg):
    if not reg.startswith('R'):
        raise ValueError(f"Invalid register: {reg}")
    num = int(reg[1:])
    if num > 15 or num < 0:
        raise ValueError(f"Invalid register: {reg}")
    return f"{num:04b}"

def imm_to_bin(imm):
    val = int(imm)
    if val > 127 or val < -128:
        raise ValueError(f"Invalid immediate value: {imm}")
    elif val < 0:
        val = (1<<8) + val
    return f"{val:08b}"

for line in src_file:
    line = line.split(';')[0].strip()
    if not line:
        continue
    tokens = re.split(r'[,\s]+', line)
    tokens = [t for t in tokens if t]
    if tokens[0] not in formats:
        print("Invalid instruction:", tokens[0])
        continue

    opcode = formats[tokens[0]]["opcode"]
    ra_bin = rb_bin = rd_bin = "0000"
    imm_bin = "00000000"

    if len(tokens[1:]) != len(formats[tokens[0]]["format"]):
        raise ValueError(f"Invalid number of arguments for instruction {tokens[0]}")

    for operand_type, operand_value in zip(formats[tokens[0]]["format"], tokens[1:]):
        if operand_type == 'rd':
            rd_bin = reg_to_bin(operand_value)
        elif operand_type == 'ra':
            ra_bin = reg_to_bin(operand_value)
        elif operand_type == 'rb':
            rb_bin = reg_to_bin(operand_value)
        elif operand_type == 'imm':
            imm_bin = imm_to_bin(operand_value)

    mem_file.write(f"{opcode}{ra_bin}{rb_bin}{rd_bin}{imm_bin}\n")

src_file.close()
mem_file.close()