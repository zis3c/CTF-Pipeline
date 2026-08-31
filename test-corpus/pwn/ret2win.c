#include <stdio.h>
#include <unistd.h>
void win(void){puts("TEST_WIN");}
int main(void){char b[32];read(0,b,128);}
