#include <stdio.h>
#include <string.h>
// gcc lolk.c -o lolk
//
// its not a direct clone of lolcat and it works a little differently.
// You can pipe into it though, and it doesnt conflict with figlet in the same way.
// Hey, lets see if it conflicts with fileRoll, and dialog. 
// the buffer size could be an issue....
const char *colors[] = {
    "\033[31m",  // Red
    "\033[33m",  // Yellow
    "\033[32m",  // Green
    "\033[36m",  // Cyan
    "\033[34m",  // Blue
    "\033[35m"   // Magenta
};

const char *reset = "\033[0m";

int main(int argc, char *argv[]) {
    int color_index = 0;

    if (argc > 1) {
        // Process the argument text
        for (int i = 0; i < strlen(argv[1]); i++) {
            printf("%s%c", colors[color_index % 6], argv[1][i]);
            color_index++;
        }
    } else {
        // Process stdin input
        char ch;
        while ((ch = getchar()) != EOF) {
            printf("%s%c", colors[color_index % 6], ch);
            color_index++;
        }
    }

    // Reset color at the end
    printf("%s\n", reset);
    return 0;
}
