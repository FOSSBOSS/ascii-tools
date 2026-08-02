# ASCII Tools - C Utilities

Small command-line programs for adding animated or colored texry are intentionally simple and have no external
runtime dependencies. They are written for POSIX-style systems and are most
useful in Linux terminals.

## Programs

| Program    | Description                                                                    |
| ---------- | ------------------------------------------------------------------------------ |
| `dialog`   | Prints text one character at a time at a fixed speed.                          |
| `fileRoll` | Reads a text file and prints it one character at a time at a selectable speed. |
| `lolk`     | Prints text using rotating ANSI terminal colors.                               |

## Requirements

* A C compiler such as GCC or Clang
* A POSIX-compatible system
* A terminal with ANSI color support for `lolk`

On Debian, Ubuntu, or Linux Mint, GCC can be installed with:

```bash
sudo apt install build-essential
```

## Building

From the `src/C` directory:

```bash
gcc -O2 dialog.c -o dialog
gcc -O2 fileRoll.c -o fileRoll
gcc -O2 lolk.c -o lolk
```

The compiled programs will be created in the current directory:

```text
dialog
fileRoll
lolk
```

## dialog

`dialog` prints a supplied string one character at a time.

### Usage

```bash
./dialog "text"
```

### Example

```bash
./dialog "This text appears one character at a time."
```

To include a line break, place the literal characters `\n` inside the quoted
text:

```bash
./dialog "First line\nSecond line"
```

The text must be passed as one argument, so text containing spaces should be
quoted.

The output delay is fixed at approximately 60 milliseconds per character.

## fileRoll

`fileRoll` reads an entire text file and prints its contents one character at a
time.

### Usage

```bash
./fileRoll filename speed
```

* `filename` is the file to display.
* `speed` is a positive integer delay multiplier.
* A larger number produces slower output.
* Values below `1` are treated as `1`.

### Examples

Display a file at the fastest available setting:

```bash
./fileRoll story.txt 1
```

Display it more slowly:

```bash
./fileRoll story.txt 5
```

The approximate delay between characters is:

```text
10 milliseconds x speed
```

For example, a speed value of `5` produces a delay of roughly 50 milliseconds
per character.

Both normal line endings in the file and literal `\n` sequences are displayed
as line breaks.

## lolk

`lolk` prints text using a repeating sequence of ANSI colors:

```text
red -> yellow -> green -> cyan -> blue -> magenta
```

By default, the color changes after every character.

### Text argument

```bash
./lolk "Rainbow text"
```

Text containing spaces must be quoted. Only one text argument should be
supplied.

### Standard input

When no text argument is given, `lolk` reads from standard input:

```bash
echo "Rainbow text" | ./lolk
```

It can also color the contents of a file:

```bash
cat story.txt | ./lolk
```

### Color interval

Use `-n` to select how many characters are printed before changing color:

```bash
./lolk -n 3 "Change color every three characters"
```

The option also works with standard input:

```bash
cat story.txt | ./lolk -n 5
```

Use a positive integer for the interval. The default is:

```text
-n 1
```

At the end of the output, `lolk` resets the terminal color and prints a final
newline.

## Installing Locally

To make the programs available from anywhere for the current user:

```bash
mkdir -p ~/.local/bin
cp dialog fileRoll lolk ~/.local/bin/
```

Ensure `~/.local/bin` is included in your `PATH`. After that, the programs can
be run without `./`:

```bash
dialog "Hello"
fileRoll story.txt 3
lolk "Colorful text"
```

## Notes

* These tools write directly to standard output and work well in shell scripts.
* `dialog` and `fileRoll` use `usleep()`, so they are intended for POSIX-style
  operating systems.
* `lolk` outputs ANSI escape sequences. Redirecting its output to a file will
  store those escape sequences in the file.
* These are small terminal-effect utilities rather than full text-processing
  applications.
