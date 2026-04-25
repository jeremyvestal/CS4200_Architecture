Memory Access Analyzer for Risc-V

Purpose ---------------
Analyzes RISC-V assembly files to track memory access patterns.

What it tracks --------
Load/Store counts | Number of memory read/write instructions 
Unique offsets    | Distinct memory locations accessed 
Average stride    | Distance between consecutive accesses 
Spatial locality  | Percentage of strides ≤ 16 bytes 
Register usage    | Which base registers are used 
Hottest offset    | Most frequently accessed address 

How to run -----------
1 | Navigate to correct directory (with file)
2 | `python vestal_mem_analyzer.py` 
3 | Enter filename when prompted 

Output example -------

Summary:

File:  file_name.s
Total instructions: 49
Memory: 21 (42.9%)
  Loads: 2
  Stores: 19
Non-memory: 28

Unique offsets: 9
Avg stride: 6.4 bytes
Spatial locality: 90.0%

Registers: x10, x11, x12
  x10: [0, 4, 8, 12, 16, 20, 24, 28, 32]
  x11: [0, 4, 8, 12, 16, 20, 24, 28, 32]
  x12: [0]

Most frequent offset: 0 (5 accesses)

Requirements ---------

Python 3
Libraries:
  os

Files ----------------

vestal_mem_analyzer.py | program file
code. s		      | example risc-v program


Author --------------
Jeremy Vestal
CS 4200 Architecture
#10 Memory Access Analyzer