#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
	/*
	 * This program rolls out text to the screen.
	 * Usage: dialog "Write some text"
	 * The text then appears character by character.
	 * 
	 * use the optional -b argument with a time in seconds
	 * to delete printed text after a time
	 * 
	 * gcc -O2 dialog.c -o dialog
	 * */
#define CHAR_DELAY 60000

void rollOut(const char *text);
void rollBack(const char *text);

int main(int argc, char **argv){
    const char *text;
    double wait_time = 0;
    int rollback = 0;

    setvbuf(stdout, NULL, _IONBF, 0);

    if (argc == 2) {
        text = argv[1];
    } else if (argc == 4 && strcmp(argv[1], "-b") == 0) {
        rollback = 1;
        wait_time = atof(argv[2]);
        text = argv[3];
    } else {
        printf("Usage: %s [-b seconds] \"text\"\n", argv[0]);
        printf("or:\nUsage: %s  \"text\"\n", argv[0]);
        return 1;
    }

    rollOut(text);

    if (rollback) {
        usleep((useconds_t)(wait_time * 1000000));
        rollBack(text);
    } else {
        printf("\n");
    }

    return 0;
}

void rollOut(const char *text){
    size_t size = strlen(text);

    for (size_t a = 0; a < size; a++) {
        if (text[a] == '\\' &&
            a + 1 < size &&
            text[a + 1] == 'n') {
            printf("\n");
            a++;
        } else {
            printf("%c", text[a]);
        }

        usleep(CHAR_DELAY);
    }
}

void rollBack(const char *text){
    size_t size = strlen(text);

    /* Track the length of every rendered line so we know where
     * to put the cursor when moving upward. */
    int lines[1024];
    int line_count = 1;
    int column = 0;

    lines[0] = 0;

    for (size_t a = 0; a < size; a++) {
        if (text[a] == '\\' &&
            a + 1 < size &&
            text[a + 1] == 'n') {
            lines[line_count - 1] = column;
            line_count++;
            lines[line_count - 1] = 0;
            column = 0;
            a++;
        } else if (text[a] == '\n') {
            lines[line_count - 1] = column;
            line_count++;
            lines[line_count - 1] = 0;
            column = 0;
        } else {
            column++;
            lines[line_count - 1] = column;
        }
    }

    int line = line_count - 1;

    for (long a = (long)size - 1; a >= 0; a--) {
        //* Literal "\n".
        if (a > 0 &&
            text[a] == 'n' &&
            text[a - 1] == '\\') {

            line--;

            printf("\033[A");       /* cursor up */
            printf("\r");           /* start of line */

            if (lines[line] > 0)
                printf("\033[%dC", lines[line]);

            a--;
            continue;
        }

        //* Actual newline embedded in the shell argument.
        if (text[a] == '\n') {
            line--;

            printf("\033[A");
            printf("\r");

            if (lines[line] > 0)
                printf("\033[%dC", lines[line]);

            continue;
        }

        printf("\b \b");
        usleep(CHAR_DELAY);
    }

    printf("\n");
}
