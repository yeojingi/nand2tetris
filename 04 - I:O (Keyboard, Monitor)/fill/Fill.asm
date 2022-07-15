// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

// Put your code here.

// 16384 - base of screen memory map
// 24576 - base of keyboard

(LOOP)
  @24576
  D=M;
  @FILL
  D; JGT
  @ERASE
  0; JMP

(FILL)
  @16384
  D=A;
  @i
  M=D;
  (FLOOP)
    // Fill 종료 조건문
    @24576
    D=A;
    @i
    D=D-M;
    @LOOP
    D;JLE
    
    @i
    A=M;
    M=-1;
    @i
    M=M+1;

    @FLOOP
    0;JMP

(ERASE)
  @16384
  D=A;
  @i
  M=D;
  (ELOOP)
    // Erase 종료 조건문
    @24576
    D=A;
    @i
    D=D-M;
    @LOOP
    D;JLE
    
    @i
    A=M;
    M=0;
    @i
    M=M+1;

    @ELOOP
    0;JMP

  @LOOP
  0; JMP