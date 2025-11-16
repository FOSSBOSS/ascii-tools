#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
// This program rolls out text to the screen.
// Usage: dialog "Write some text"
// The text then appears character by character.

void rollOut(char *startup);

	
int main(int argc, char **argv){
		if(argc !=2){
		printf("Usage: %s text to encode in qoutes\n",argv[0]);
		return 0; 
		}
	char *startup= argv[1];
rollOut(startup);
return 0;
}

void rollOut(char *startup){
	usleep(10000);
	int size = strlen(startup);
	for (int a = 0; a < size; a++){
		if(startup[a]=='\\'&& startup[a+1]=='n'){
			printf("\n");
			a=a+2;
			}
    	setvbuf(stdout, NULL, _IONBF, 0);
		printf("%c", startup[a]);
		usleep(60000);
	}
	printf("\n");
}
