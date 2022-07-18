#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define BUFF_SIZE 200
#define CODE_SIZE 100

void generate_inter_fileName(char*, const char* );
void generate_output_fileName(char*, const char* );
void symboleTableInitialize();
void firstPass(FILE *);
void getLabel(char*, const char* );
void secondPass(FILE*, FILE* );
void allocSymbol(char *, const char* );
void eraseSpace(char *, const char* );
void parser(FILE* , FILE* );
enum commandType sortCommand(const char* );
int getSymbol(const char*, enum commandType );
void getCode(char[] , char[] , char[] , const char* );
char* convertToBinary(char* , char[] , char[] , char[] );
char* dec2bin_char(char* , int );

enum commandType {
  A_COMMAND,
  C_COMMAND,
  L_COMMAND,
  WHITE_SPACE
};

typedef struct symbolRow {
  char label[50];
  int addr;
} symbolRow_t;

symbolRow_t symbolTable[3000];
int symbolTable_len = 0;
int alloc_RAM = 16;

int main(int argc, char** args)
{
  FILE *fp_read;
  FILE *fp_inter;
  FILE *fp_out;
  char* fn = malloc(sizeof(char) * 20);
  char* fn_inter = malloc(sizeof(char) * 20);
  char* fn_output = malloc(sizeof(char) * 20);
  char* line = malloc(sizeof(char) * BUFF_SIZE);

  if (argc < 2) {
    printf("error: no argument included\n");
    return 1;
  }

  fn = strcat(fn, args[1]);
  generate_inter_fileName(fn_inter, fn);
  generate_output_fileName(fn_output, fn);

  fp_read = fopen(fn, "r");
  fp_inter = fopen(fn_inter, "w");
  fp_out = fopen(fn_output, "w");

  if (fp_read == NULL) {
    printf("error: no file exits %s\n", fn);
    return 1;
  }

  symboleTableInitialize();
  
  firstPass(fp_read);
  fclose(fp_read);
  fp_read = fopen(fn, "r");

  secondPass(fp_read, fp_inter);
  fclose(fp_read);
  fclose(fp_inter);
  fp_read = fopen(fn_inter, "r");

  parser(fp_read, fp_out);

  fclose(fp_read);
  fclose(fp_out);

  free(fn);
  free(fn_inter);
  free(fn_output);
  free(line);
}

void generate_inter_fileName(char* fn_o, const char* fn)
{
  fn_o = strncpy(fn_o, fn, strlen(fn) - 4);
  fn_o[strlen(fn_o)] = '\0';
  fn_o = strcat(fn_o, ".inter");
}

void generate_output_fileName(char* fn_o, const char* fn)
{
  fn_o = strncpy(fn_o, fn, strlen(fn) - 4);
  fn_o[strlen(fn_o)] = '\0';
  fn_o = strcat(fn_o, ".hack");
}

void symboleTableInitialize()
{
  int addr = 0;
  strcpy(symbolTable[symbolTable_len].label, "SP");
  symbolTable[symbolTable_len].addr = symbolTable_len;
  symbolTable_len++;

  strcpy(symbolTable[symbolTable_len].label, "LCL");
  symbolTable[symbolTable_len].addr = symbolTable_len;
  symbolTable_len++;

  strcpy(symbolTable[symbolTable_len].label, "ARG");
  symbolTable[symbolTable_len].addr = symbolTable_len;
  symbolTable_len++;

  strcpy(symbolTable[symbolTable_len].label, "THIS");
  symbolTable[symbolTable_len].addr = symbolTable_len;
  symbolTable_len++;

  strcpy(symbolTable[symbolTable_len].label, "THAT");
  symbolTable[symbolTable_len].addr = symbolTable_len;
  symbolTable_len++;


  for (int i = 0; i < 10; i++) {
    symbolTable[symbolTable_len].label[0] = 'R';
    symbolTable[symbolTable_len].label[1] = i+48;
    symbolTable[symbolTable_len].label[2] = '\0';

    symbolTable[symbolTable_len].addr = i;
    symbolTable_len++;
  }

  for (int i = 10; i < 16; i++) {
    symbolTable[symbolTable_len].label[0] = 'R';
    symbolTable[symbolTable_len].label[1] = '1';
    symbolTable[symbolTable_len].label[2] = i-10+48;
    symbolTable[symbolTable_len].label[3] = '\0';

    symbolTable[symbolTable_len].addr = i;
    symbolTable_len++;
  }

  strcpy(symbolTable[symbolTable_len].label, "SCREEN");
  symbolTable[symbolTable_len].addr = 16384;
  symbolTable_len++;

  strcpy(symbolTable[symbolTable_len].label, "KBD");
  symbolTable[symbolTable_len].addr = 24576;
  symbolTable_len++;

}

void firstPass(FILE *fp_read) {
  char* line = malloc(sizeof(char) * BUFF_SIZE);
  enum commandType curType;
  char label[BUFF_SIZE];
  int line_num = 0;

  while (fgets(line, BUFF_SIZE, fp_read) != NULL) {
    curType = sortCommand(line);

    switch (curType) {
      case A_COMMAND:
        line_num++;
        break;
      case C_COMMAND:
        line_num++;
        break;
      case L_COMMAND:
        getLabel(&label, line);
        strcpy(symbolTable[symbolTable_len].label, label);
        symbolTable[symbolTable_len].addr = line_num;
        symbolTable_len++;
        break;
      case WHITE_SPACE:
        break;
    }
  }

  free(line);
}

void getLabel(char* label, const char* line)
{
  char* cur = line;
  int i = 0;
  cur++;

  while (*cur != ')') {
    label[i++] = *cur;
    cur ++;
  }

  label[i] = '\0';
}

void secondPass(FILE* fp_read, FILE* fp_inter)
{
  char* line = malloc(sizeof(char) * BUFF_SIZE);
  char* new_line = malloc(sizeof(char) * BUFF_SIZE);
  enum commandType curType;
  char var[BUFF_SIZE];

  while (fgets(line, BUFF_SIZE, fp_read) != NULL) {
    curType = sortCommand(line);

    switch (curType) {
      case A_COMMAND:
        allocSymbol(new_line, line);
        fprintf(fp_inter, "%s", new_line);
        break;
      case C_COMMAND:
        eraseSpace(new_line, line);
        fprintf(fp_inter, "%s", new_line);
        break;
      case L_COMMAND:
        break;
      case WHITE_SPACE:
        break;
    }
  }

  free(new_line);
  free(line);
}

void allocSymbol(char* new_line, const char* line)
{
  char* cursor = line;
  char str[BUFF_SIZE];
  int i;
  int isInTable = 0;
  
  while (*cursor == ' ') {
    cursor++;
  }

  cursor++;
  for (i = 0; 1; i++) {
    if (*cursor == 13 || *cursor==10 || *cursor == ' ') {
      break;
    }
    str[i] = *cursor++;
  }
  str[i] = '\0';

  // if charcacter
  if (str[0] > 57) {
    for (i = 0; i < symbolTable_len; i++) {
      if (strcmp(symbolTable[i].label, str) == 0) {
        isInTable = 1;
        break;
      }
    }

    if (isInTable == 1) {
      sprintf(new_line, "@%d\n", symbolTable[i].addr);
    }
    else if (isInTable == 0) {
      strcpy(symbolTable[symbolTable_len].label, str);
      sprintf(new_line, "@%d\n", alloc_RAM);
      symbolTable[symbolTable_len].addr = alloc_RAM++;
      symbolTable_len++;
    }
  }
  else {
    sprintf(new_line, "@%s\n", str);
  }
}

void eraseSpace(char* new_line, const char* line)
{
  char* cursor = line;
  char str[BUFF_SIZE];
  int i;
  
  while (*cursor == ' ') {
    cursor++;
  }

  for (i = 0; 1; i++) {
    if (*cursor == 13 || *cursor == ' ') {
      break;
    }
    str[i] = *cursor++;
  }
  str[i] = '\0';

  sprintf(new_line, "%s\n", str);
}

void parser(FILE *fp_read, FILE *fp_out) {
  char* line = malloc(sizeof(char) * BUFF_SIZE);
  enum commandType curType;
  char dest[CODE_SIZE], comp[CODE_SIZE], jump[CODE_SIZE];
  int symbol;
  char bin[17];

  while (fgets(line, BUFF_SIZE, fp_read) != NULL) {
    curType = sortCommand(line);

    switch (curType) {
      case A_COMMAND:
        symbol = getSymbol(line, curType);
        // bin = dec2bin_char(symbol);
        dec2bin_char(&bin, symbol);
        fprintf(fp_out, "%s\n", bin);
        break;
      case C_COMMAND:
        getCode(dest, comp, jump, line);
        // bin = convertToBinary(dest, comp, jump);

        convertToBinary(&bin, dest, comp, jump);
        fprintf(fp_out, "%s\n", bin);
        break;
      case L_COMMAND:
        break;
      case WHITE_SPACE:
        break;
    }
  }

  free(line);
}

enum commandType sortCommand(const char* line) {
  enum commandType type;
  char* cur;

  cur = line;
  while (1) {
    if (*cur == ' ') {
      cur++;
    } else {
      break;
    }
  }

  if (*cur == '@') {
    type = A_COMMAND;
  }
  else if (*cur == '(') {
    type = L_COMMAND;
  }
  else if ((*cur >= 48 && *cur <= 57) || (*cur == 'A' || *cur == 'M' || *cur == 'D' || *cur =='J')) {
    type = C_COMMAND;
  }
  else {
    type = WHITE_SPACE;
  }

  return type;
}

int getSymbol(const char* line, enum commandType curType)
{
  char* cursor = line;
  char str[BUFF_SIZE];
  int i = 0;

  cursor++;
  for (i = 0; 1; i++) {
    if (*cursor == 13 || *cursor == 10) {
      break;
    }
    str[i] = *cursor++;
  }
  str[i] = '\0';

  return atoi(str);
  
}

void getCode(char dest[], char comp[], char jump[], const char* line)
{
  char* cursor = line;
  int i = 0;
  char code[CODE_SIZE];
  int isEqual = 0;
  int isColon = 0;

  strcpy(dest, "null0");
  strcpy(jump, "null");

  for (i = 0; 1; i++) {
    if (*cursor == '=') {
      isEqual = 1;
      code[i] = '\0';
      strcpy(dest, code);
      i=-1;
    }
    else if (*cursor == ';') {
      isColon = 1;
      code[i] = '\0';
      strcpy(comp, code);
      i=-1;
    }
    else if (*cursor == 13 || *cursor == 10) {
      if (isColon == 0) {
        code[i] = '\0';
        strcpy(comp, code);
      } else {
        code[i] = '\0';
        strcpy(jump, code);
      }
      break;
    } else {
      code[i] = *cursor;
    }

    cursor++;
  }
}

char* convertToBinary(char* out, char dest[], char comp[], char jump[])
{
  char bin[17];
  char buff[17];
  char* buff_comp = malloc(sizeof(char) * BUFF_SIZE);
  char* cur;
  
  bin[16] = '\0';
  bin[0] = '1';
  bin[1] = '1';
  bin[2] = '1';

  // comp
  if (strcmp(comp, "0") == 0) {
    strcpy(buff_comp, "0101010");
  }
  else if (strcmp(comp, "1") == 0) {
    strcpy(buff_comp, "0111111");
  }
  else if (strcmp(comp, "-1") == 0) {
    strcpy(buff_comp, "0111010");
  }
  else if (strcmp(comp, "D") == 0) {
    strcpy(buff_comp, "0001100");
  }
  else if (strcmp(comp, "A") == 0) {
    strcpy(buff_comp, "0110000");
  }
  else if (strcmp(comp, "!D") == 0) {
    strcpy(buff_comp, "0001101");
  }
  else if (strcmp(comp, "!A") == 0) {
    strcpy(buff_comp, "0110001");
  }
  else if (strcmp(comp, "-D") == 0) {
    strcpy(buff_comp, "0001111");
  }
  else if (strcmp(comp, "-A") == 0) {
    strcpy(buff_comp, "0110011");
  }
  else if (strcmp(comp, "D+1") == 0) {
    strcpy(buff_comp, "0011111");
  }
  else if (strcmp(comp, "A+1") == 0) {
    strcpy(buff_comp, "0110111");
  }
  else if (strcmp(comp, "D-1") == 0) {
    strcpy(buff_comp, "0001110");
  }
  else if (strcmp(comp, "A-1") == 0) {
    strcpy(buff_comp, "0110010");
  }
  else if (strcmp(comp, "D+A") == 0) {
    strcpy(buff_comp, "0000010");
  }
  else if (strcmp(comp, "D-A") == 0) {
    strcpy(buff_comp, "0010011");
  }
  else if (strcmp(comp, "A-D") == 0) {
    strcpy(buff_comp, "0000111");
  }
  else if (strcmp(comp, "D&A") == 0) {
    strcpy(buff_comp, "0000000");
  }
  else if (strcmp(comp, "D|A") == 0) {
    strcpy(buff_comp, "0010101");
  }
  else if (strcmp(comp, "M") == 0) {
    strcpy(buff_comp, "1110000");
  }
  else if (strcmp(comp, "!M") == 0) {
    strcpy(buff_comp, "1110001");
  }
  else if (strcmp(comp, "-M") == 0) {
    strcpy(buff_comp, "1110011");
  }
  else if (strcmp(comp, "M+1") == 0) {
    strcpy(buff_comp, "1110111");
  }
  else if (strcmp(comp, "M-1") == 0) {
    strcpy(buff_comp, "1110010");
  }
  else if (strcmp(comp, "D+M") == 0) {
    strcpy(buff_comp, "1000010");
  }
  else if (strcmp(comp, "D-M") == 0) {
    strcpy(buff_comp, "1010011");
  }
  else if (strcmp(comp, "M-D") == 0) {
    strcpy(buff_comp, "1000111");
  }
  else if (strcmp(comp, "D&M") == 0) {
    strcpy(buff_comp, "1000000");
  }
  else if (strcmp(comp, "D|M") == 0) {
    strcpy(buff_comp, "1010101");
  }

  cur = buff_comp;
  for (int i = 0; i < 7; i++) {
    bin[i+3] = *cur++;
  }

  // dest
  if (strcmp(dest, "null0") == 0) {
    strcpy(buff_comp, "000");
  }
  else if (strcmp(dest, "M") == 0) {
    strcpy(buff_comp, "001");
  }
  else if (strcmp(dest, "D") == 0) {
    strcpy(buff_comp, "010");
  }
  else if (strcmp(dest, "MD") == 0) {
    strcpy(buff_comp, "011");
  }
  else if (strcmp(dest, "A") == 0) {
    strcpy(buff_comp, "100");
  }
  else if (strcmp(dest, "AM") == 0) {
    strcpy(buff_comp, "101");
  }
  else if (strcmp(dest, "AD") == 0) {
    strcpy(buff_comp, "110");
  }
  else if (strcmp(dest, "AMD") == 0) {
    strcpy(buff_comp, "111");
  }

  cur = buff_comp;
  for (int i = 0; i < 3; i++) {
    bin[i+10] = *cur++;
  }

  // jump
  if (strcmp(jump, "null") == 0) {
    strcpy(buff_comp, "000");
  }
  else if (strcmp(jump, "JGT") == 0) {
    strcpy(buff_comp, "001");
  }
  else if (strcmp(jump, "JEQ") == 0) {
    strcpy(buff_comp, "010");
  }
  else if (strcmp(jump, "JGE") == 0) {
    strcpy(buff_comp, "011");
  }
  else if (strcmp(jump, "JLT") == 0) {
    strcpy(buff_comp, "100");
  }
  else if (strcmp(jump, "JNE") == 0) {
    strcpy(buff_comp, "101");
  }
  else if (strcmp(jump, "JLE") == 0) {
    strcpy(buff_comp, "110");
  }
  else if (strcmp(jump, "JMP") == 0) {
    strcpy(buff_comp, "111");
  }

  cur = buff_comp;
  for (int i = 0; i < 3; i++) {
    bin[i+13] = *cur++;
  }

  strcpy(out, bin);

  free(buff_comp);
}

char* dec2bin_char(char* out, int dec)
{
  int coef = 0;
  char bin_without_0[17];
  char bin[17];
  bin[0] = '0';
  bin[16] = '\0';

  for (int i = 0; i < 15; i++) {
    if (dec > 0) {
      coef = dec % 2;
      if (coef == 1) {
        dec = (dec - 1) / 2;
        bin[15-i] = '1';
      } else if (coef == 0) {
        dec = dec / 2;
        bin[15-i] = '0';
      }
    }
    else {
      bin[15-i] = '0';
    }
  }

  strcpy(out, bin);
}