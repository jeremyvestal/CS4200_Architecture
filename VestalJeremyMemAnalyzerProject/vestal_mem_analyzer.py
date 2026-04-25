#Jeremy Vestal
#Architecture Project
#Takes in a .s file with risc-v instructions and counts memory accesses, and displays stats on them.

import os

#I keep the stats local as its easier to follow
total_instructions = 0
total_loads = 0
total_stores = 0
unknown_count = 0
address_counts = {}
strides = []
last_offset = None
register_accesses = {}
registers_used = []

#Takes a line string of assembly code (1 inst) returns a tuple tuple that has type register and offset, 
#if it is a nonmem inst it returns a false flag tuple
def parse_memory_instruction(line):
    global unknown_count
    
    #checks for empty line or comment line
    if not line == "" and not line.startswith('//'):
        #splits the line into a list of sections op, reg, off
        parts = line.split()
        #extracts op
        op = parts[0].lower()
        
        #checks if the operation is either load or store 
        if op in ['lw', 'lb', 'lh', 'lbu', 'lhu', 'sw', 'sb', 'sh']:
            #Gets the memory part of inst, handles the commas before
            if len(parts) >= 3 and ',' in parts[1]:
                mem_part = parts[2]
            else:
                mem_part = parts[1]
            #checks for the format parentheses, if they arent there its unknown 
            if '(' not in mem_part or ')' not in mem_part:
                values = (False, None, None, None)
            else:
                #indexes each of the parentheses to extract the offset and register
                start = mem_part.find('(')
                end = mem_part.find(')')
            
                
                #extracts offset and reg using parentheses
                offset_str = mem_part[:start]
                reg = mem_part[start+1:end]
                
                #checks for missing off
                if offset_str == '':
                    offset = 0
                else:
                    offset = int(offset_str)
                #Returns a tuple with the line stats
                values = (True, op, reg, offset)
        else:
            #unknown tuple 
            unknown_count = unknown_count + 1
            values = (False, None, None, None)
    else:
        #invalid line tuple w/o updating unknown count
        values = (False, None, None, None)
    return values

#takes each value in a tuple and updates the stat counters for analysis and summary
def update_stats(is_memory, op_type, reg, offset):
    #all globals updated
    global total_loads, total_stores, last_offset
    global address_counts, strides, register_accesses, registers_used
    
    #ensures the instruction is a memory 
    if is_memory:
                
        #count loads vs stores by checking op type and incrementing respective counter
        if op_type in ['lw', 'lb', 'lh', 'lbu', 'lhu']:
            total_loads = total_loads + 1
        else:
            total_stores = total_stores + 1
        
        #checks for a preexisting offset, or adds to list if not, increments count for that offset
        if offset in address_counts:
            address_counts[offset] = address_counts[offset] + 1
        else:
            address_counts[offset] = 1
        
        #tracks the stride by comparing the current offset to the last one, and adds it to the strides list 
        if last_offset is not None:
            stride = abs(offset - last_offset)
            strides.append(stride)
        last_offset = offset
        
        #Checks if the reg was already used, increments if so, otherwise adds to list
        if reg not in register_accesses:
            register_accesses[reg] = {}
            registers_used.append(reg)
        #checks for a preexisting offset for that register, or adds to list if not, increments count for that offset
        if offset in register_accesses[reg]:
            register_accesses[reg][offset] = register_accesses[reg][offset] + 1
        else:
            register_accesses[reg][offset] = 1

#Prints summary of all of the stats
def print_summary(filename):
    global total_instructions, total_loads, total_stores, unknown_count
    global address_counts, strides, register_accesses, registers_used
    
    #file stats
    print("\nSummary:")
    print("\nFile: " + filename)
    
    mem_insts = total_loads + total_stores
    print("Total instructions: " + str(total_instructions))
    print("Memory: " + str(mem_insts) + " (" + str(round(mem_insts * 100.0 / total_instructions, 1)) + "%)")
    print("  Loads: " + str(total_loads))
    print("  Stores: " + str(total_stores))
    print("Non-memory: " + str(unknown_count))
    
    #checks for mem isntructions before printing mem-specific stats
    if not mem_insts == 0:
           
        print("\nUnique offsets: " + str(len(address_counts)))
        
        #strides and locality
        if len(strides) > 0:
            avg_stride = sum(strides) / len(strides)
            small = len([s for s in strides if s <= 16])
            locality = small * 100.0 / len(strides)
            print("Avg stride: " + str(round(avg_stride, 1)) + " bytes")
            print("Spatial locality: " + str(round(locality, 1)) + "%")
        
        print("\nRegisters: " + ", ".join(registers_used))
        for reg in registers_used:
            offsets = sorted(register_accesses[reg].keys())
            print("  " + reg + ": " + str(offsets))
        
        #Gets hightst frequency offset by finding the max value in the address_counts dict and printing it with its count
        highest = max(address_counts, key=address_counts.get)
        print("\nMost frequent offset: " + str(highest) + " (" + str(address_counts[highest]) + " accesses)")
    

#traces the file line by line calling all functions to analyze and print stats
def analyze_memory_trace(filename):
    #globals
    global total_instructions, total_loads, total_stores, unknown_count
    global address_counts, strides, last_offset, register_accesses, registers_used
    
    #reset all stats for each file 
    total_instructions = 0
    total_loads = 0
    total_stores = 0
    unknown_count = 0
    address_counts = {}
    strides = []
    last_offset = None
    register_accesses = {}
    registers_used = []
    
    #checks to open file, it will error file is non-existent, so it checks for common extensions and adds them if needed
    if not os.path.exists(filename):
        if os.path.exists(filename + ".s"):
            filename = filename + ".s"
        elif os.path.exists(filename + ".txt"):
            filename = filename + ".txt"
        else:
            #get out!!!
            print("File not found.")
            return
    #opens file for reading
    f = open(filename, 'r')
    
    print("\nInstruction trace:")
   
    #inits at the first line, then iterates line by line, analyzing each line
    line_num = 0
    for line in f:
        line = line.strip()

        #makes sure empty lines and comments are ignored
        if not line == "" and not line.startswith('//'):

            #keeps track of line num for trace and total insts        
            line_num = line_num + 1
            total_instructions = total_instructions + 1
            
            #saves each necessary value from the instruction
            is_mem, op_type, reg, offset = parse_memory_instruction(line)
            
            #checks if it is a memory value, if it is it will update the mem-specific stats
            if is_mem:
                update_stats(is_mem, op_type, reg, offset)
                print("Line " + str(line_num) + ": " + op_type + " reg=" + reg + " offset=" + str(offset))
            else:
                print("Line " + str(line_num) + ": Unknown")
    
    f.close()
    print_summary(filename)

#main program, prompts for a file, starts analysis
print("Jeremy's Mem Access Analyzer")
filename = input("Enter filename to analyze: ").strip()
analyze_memory_trace(filename)
#pause to let user read
input("\nPress Enter to exit...")