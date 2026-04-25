// Matrix addition program - demonstrates sequential memory access
// This program adds two 3x3 matrices and stores the result

// Initialize matrix A values (9 elements)
addi x1, x0, 1
sw x1, 0(x10)
addi x1, x0, 2
sw x1, 4(x10)
addi x1, x0, 3
sw x1, 8(x10)
addi x1, x0, 4
sw x1, 12(x10)
addi x1, x0, 5
sw x1, 16(x10)
addi x1, x0, 6
sw x1, 20(x10)
addi x1, x0, 7
sw x1, 24(x10)
addi x1, x0, 8
sw x1, 28(x10)
addi x1, x0, 9
sw x1, 32(x10)

// Initialize matrix B values (9 elements)
addi x1, x0, 9
sw x1, 0(x11)
addi x1, x0, 8
sw x1, 4(x11)
addi x1, x0, 7
sw x1, 8(x11)
addi x1, x0, 6
sw x1, 12(x11)
addi x1, x0, 5
sw x1, 16(x11)
addi x1, x0, 4
sw x1, 20(x11)
addi x1, x0, 3
sw x1, 24(x11)
addi x1, x0, 2
sw x1, 28(x11)
addi x1, x0, 1
sw x1, 32(x11)

// Matrix addition loop
addi x12, x0, 0      // loop counter
addi x13, x0, 9      // total iterations (3x3 = 9)

loop:
    // Load from matrix A
    lw x2, 0(x10)
    lw x3, 0(x11)
    
    // Add them
    add x4, x2, x3
    
    // Store result in matrix C
    sw x4, 0(x12)
    
    // Move to next element
    addi x10, x10, 4
    addi x11, x11, 4
    addi x12, x12, 4
    addi x13, x13, -1
    
    // Loop until done
    bne x13, x0, loop

// End of program
addi x0, x0, 0