#include <stdio.h>
#include <string.h>
#include <stdlib.h>
// now with -n arg for number of characters to skipp before changing colour
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
    int shift_interval = 1;  // Default to 1 character before color change
    char *input_text = NULL;  // Pointer for text input if provided as argument

    // Parse arguments for optional -n flag and text input
    for (int i = 1; i < argc; i++) {
        if (strcmp(argv[i], "-n") == 0 && i + 1 < argc) {
            shift_interval = atoi(argv[i + 1]);
            i++;  // Skip the next argument as it's part of -n
        } else {
            input_text = argv[i];  // Treat any remaining argument as text input
        }
    }

    int char_count = 0;

    if (input_text) {
        // Process the argument text if provided
        for (int i = 0; i < strlen(input_text); i++) {
            printf("%s%c", colors[color_index % 6], input_text[i]);
            char_count++;
            if (char_count == shift_interval) {
                color_index++;
                char_count = 0;
            }
        }
    } else {
        // Process stdin input if no text argument is provided
        char ch;
        while ((ch = getchar()) != EOF) {
            printf("%s%c", colors[color_index % 6], ch);
            char_count++;
            if (char_count == shift_interval) {
                color_index++;
                char_count = 0;
            }
        }
    }

    // Reset color at the end
    printf("%s\n", reset);
    return 0;
}
