#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
// Prolly port this to python...
// Ok look, read a file and roll the text out to the screen. 
// Usage: fileRoll filename

void rollOut(char *startup);
int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s filename\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "r");
    if (fp == NULL) {
        printf("Error: could not open file '%s'\n", argv[1]);
        return 1;
    }

    // Find the length of the file
    fseek(fp, 0L, SEEK_END);
    long filesize = ftell(fp);
    fseek(fp, 0L, SEEK_SET);

    // Allocate a buffer to store the file contents
    char *buffer = malloc(filesize + 1);
    if (buffer == NULL) {
        printf("Error: could not allocate memory\n");
        return 1;
    }

    // Read the file into the buffer
    fread(buffer, filesize, 1, fp);
    buffer[filesize] = '\0';
    fclose(fp);
    // Print the contents of the buffer
    //printf("%s", buffer);
    rollOut(buffer);
    free(buffer);
    return 0;
}

void rollOut(char *startup){
	usleep(6000);
	int size = strlen(startup);
	for (int a = 0; a < size; a++){
		if(startup[a]=='\\'&& startup[a+1]=='n'){
			printf("\n");
			a=a+2;
			}
    	setvbuf(stdout, NULL, _IONBF, 0);
		printf("%c", startup[a]);
		usleep(10000);
	}
	printf("\n");
}
