#!/usr/bin/env python3

"""
This is a very simple TAC to x64 assembly pass. It only handles straightline
code and a single main() function.

Usage: python3 tac2asm.py tacfile.json
Produces: tacfile.s (assembly) and tacfile.exe (executable)
Requires: a working gcc
"""

import json
import sys
from ast2tac import Instr
from typing import List
import sys
import os

register_temporaries = {1:"rdi", 2:"rsi", 3:"rdx", 4:"rcx", 5:"r8", 6:"r9"}

jcc = {"je": (lambda arg, label: ['movq $0, %r11',
                                  f'cmpq %r11, {arg}',
                                  f'je {label}']),
       "jne": (lambda arg, label: ['movq $0, %r11',
                                   f'cmpq %r11, {arg}',
                                   f'jne {label}']),
       "jl": (lambda arg, label: ['movq $0, %r11',
                                  f'cmpq %r11, {arg}',
                                  f'jl {label}']),
       "jle": (lambda arg, label: ['movq $0, %r11',
                                   f'cmpq %r11, {arg}',
                                   f'jle {label}']),
       "jg": (lambda arg, label: ['movq $0, %r11',
                                   f'cmpq %r11, {arg}',
                                   f'jg {label}']),
       "jge": (lambda arg, label: ['movq $0, %r11',
                                    f'cmpq %r11, {arg}',
                                    f'jge {label}'])
       }


binops = {'add': 'addq',
          'sub': 'subq',
          'mul': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                      f'imulq {rb}',
                                      f'movq %rax, {rd}']),
          'div': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                      f'cqto',
                                      f'idivq {rb}',
                                      f'movq %rax, {rd}']),
          'mod': (lambda ra, rb, rd: [f'movq {ra}, %rax',
                                      f'cqto',
                                      f'idivq {rb}',
                                      f'movq %rdx, {rd}']),
          'and': 'andq',
          'or': 'orq',
          'xor': 'xorq',
          'shl': (lambda ra, rb, rd: [f'movq {ra}, %r11',
                                      f'movq {rb}, %rcx',
                                      f'salq %cl, %r11',
                                      f'movq %r11, {rd}']),
          'shr': (lambda ra, rb, rd: [f'movq {ra}, %r11',
                                      f'movq {rb}, %rcx',
                                      f'sarq %cl, %r11',
                                      f'movq %r11, {rd}'])}
unops = {'neg': 'negq',
         'not': 'notq'}


def lookup_temp(temp, temp_map):
    assert (isinstance(temp, str) and
            temp[0] == '%' and
            temp[1:].isnumeric()), temp
    return temp_map.setdefault(temp, f'{-8 * (len(temp_map) + 1)}(%rbp)')


def tac_to_asm(tac_instrs):
    """
    Get the x64 instructions correspondign to the TAC instructions
    """
    temp_map = dict()
    asm = []
    

    for instr in tac_instrs:
        opcode = instr["opcode"]
        args = instr["args"]
        result = instr["result"]
        if opcode == 'nop':
            pass
        elif opcode == "param" :
            # get stack slot location of the arg
            arg = lookup_temp(args[1], temp_map)
            # create new temporary or fill the old one if we already created one
            result = lookup_temp("%-"+str(arg[0]) , temp_map)
            # copy the arg to stack slot of temporary
            asm.append(f'movq {arg}, %r11')
            asm.append(f'movq %r11, {result}')
            
        
        elif opcode == "call" :
            # order the list using by decreasing oreder of the first element of the tupple 
            # put the 7 first arguments into the registers (start by end of the list)
            # when done with the 7 first, start by beginning of the list 
            # push smthg useless if not 16 bytes alignes (nb of args is not even)
            # empty the list of call arguments 

            for index_arg in range(1,min(6,args[1])+1) :
                arg_temp = lookup_temp("%-"+index_arg, temp_map)
                asm.append(f'movq {arg_temp}, {register_temporaries[index_arg]}')
            
            for index_arg in range(args[1], min(6,args[1]),-1) :
                arg_temp = lookup_temp("%-"+index_arg, temp_map) 
                asm.append(f'pushq {arg_temp}')
            
            if args[1] > 6 and (args[1]%2) :
                asm.append(f'pushq $0')
            
            asm.append(f'callq {arg[0]}')
            asm.append(f'addq ${  8  *  (args[1]-6) + args[1]%2 }, %rsp')
            asm.append(f'movq %rax, {result[0]}')
            

        
        elif opcode == 'const':
            assert len(args) == 1 and isinstance(args[0], int)
            result = lookup_temp(result, temp_map)
            asm.append(f'movq ${args[0]}, {result}')
        elif opcode == 'label':
            assert len(args) == 1
            asm.append(f'{args[0][1:]}:')
        elif opcode == 'jmp':
            assert len(args) == 1
            asm.append(f'jmp {args[0][1:]}')
        elif opcode in jcc:
            jump = jcc[opcode]
            assert len(args) == 2
            arg = lookup_temp(args[0], temp_map)
            label = args[1][1:]
            asm.extend(jump(arg, label))
        elif opcode == 'copy':
            assert len(args) == 1
            arg = lookup_temp(args[0], temp_map)
            result = lookup_temp(result, temp_map)
            asm.append(f'movq {arg}, %r11')
            asm.append(f'movq %r11, {result}')
        elif opcode in binops:
            assert len(args) == 2
            arg1 = lookup_temp(args[0], temp_map)
            arg2 = lookup_temp(args[1], temp_map)
            result = lookup_temp(result, temp_map)
            proc = binops[opcode]
            if isinstance(proc, str):
                asm.extend([f'movq {arg1}, %r11',
                            f'{proc} {arg2}, %r11',
                            f'movq %r11, {result}'])
            else:
                asm.extend(proc(arg1, arg2, result))
        elif opcode in unops:
            assert len(args) == 1
            arg = lookup_temp(args[0], temp_map)
            result = lookup_temp(result, temp_map)
            proc = unops[opcode]
            asm.extend([f'movq {arg}, %r11',
                        f'{proc} %r11',
                        f'movq %r11, {result}'])
        elif opcode == 'print':
            assert len(args) == 1
            assert result == None
            arg = lookup_temp(args[0], temp_map)
            asm.extend(["pushq %rdi",
                        "pushq %rax",
                        f'movq {arg}, %rdi',
                        "callq bx_print_int",
                        "popq %rax",
                        "popq %rdi"])
        else:
            assert False, f'unknown opcode: {opcode}'
    asm[:0] = [f'pushq %rbp',
               f'movq %rsp, %rbp',
               f'subq ${8 * len(temp_map)}, %rsp'] 
    asm.extend([f'Lret:',
                f'movq %rbp, %rsp',
                f'popq %rbp',
                f'xorq %rax, %rax',
                f'retq'])
    return asm

def compile_tac(tac: List[Instr], fname: str, write: bool=True):
    assert isinstance(tac, list) and len(tac) == 1, tac
    tac = tac[0]
    assert 'proc' in tac and tac['proc'] == '@main', tac
    asm = ['\t' + line for line in tac_to_asm(tac['body'])]
    if write:
        asm[:0] = [f'\t.section .rodata',
                   f'.lprintfmt:',
                   f'\t.string "%ld\\n"',
                   f'\t.text',
                   f'\t.globl main',
                   f'main:']
        sname = fname[:-3] + '.s'
        with open(sname, 'w') as afp:
            print(*asm, file=afp, sep='\n')
        print(f'{fname} -> {sname}')


def compile_tac_from_json(fname):
    assert fname.endswith('.tac.json')
    with open(fname, 'rb') as fp:
        tjs = json.load(fp)
    assert isinstance(tjs, list) and len(tjs) == 1, tjs
    tjs = tjs[0]
    assert 'proc' in tjs and tjs['proc'] == '@main', tjs
    asm = ['\t' + line for line in tac_to_asm(tjs['body'])]
    asm[:0] = [f'\t.section .rodata',
               f'.lprintfmt:',
               f'\t.string "%ld\\n"',
               f'\t.text',
               f'\t.globl main',
               f'main:']
    sname = fname[:-9] + '.s'
    with open(sname, 'w') as afp:
        print(*asm, file=afp, sep='\n')
    print(f'{fname} -> {sname}')



if __name__ == "__main__":
    compile_tac_from_json(sys.argv[1])


