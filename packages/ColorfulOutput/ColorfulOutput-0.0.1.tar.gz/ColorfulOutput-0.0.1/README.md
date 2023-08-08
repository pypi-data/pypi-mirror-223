ColorfulOutput
=============

<p align="center">
    <img src="Images/Logo/ColorfulOutputLogo.png" width=500>
</p>

A python library that adds colors to your console prints.

# Author

- [@RasseTheBoy](https://github.com/RasseTheBoy)

# Installation

```bash
pip install ColorfulOutput
# or
pip3 install ColorfulOutput
```

# Usage

The library contains methods that you can use to color your **console** text.  
[**These "colored" strings should only be used for console prints, and not for anything else!**](#known-issues)

```python
import ColorfulOutput as cc

text = cc.HEADER("Hello World!")
print(text)
```

```python
from ColorfulOutput import BLUE, RED

print(BLUE("This is all blue text!"))
print(RED("This is all red text!"))
```

```python
from ColorfulOutput import CYAN, YELLOW, RED, BOLD, UNDERLINE

text = f'{BOLD("Never")} {YELLOW("gonna")} {UNDERLINE("give")} {RED("you")} {CYAN("up")}!'

print(text)
```

# Methods

- `HEADER(text)`
- `BLUE(text)`
- `CYAN(text)`
- `GREEN(text)`
- `YELLOW(text)`
- `RED(text)`
- `BOLD(text)`
- `UNDERLINE(text)`

# Known issues!

## Repr

The methods will return a text string that seems like a normal text to the console, but it is actually a string with special characters that makes the text colored. This means that when you use the `repr()` function, it will return a string with special characters instead of the actual text.

This also means that when you use the `!r` format specifier, it will return a string with special characters instead of the actual text.

```python
from ColorfulOutput import BLUE

clean_text = "Hello World!"
color_text = BLUE(clean_text)

print(repr(clean_text))
# Output: 'Hello World!'

print(f'{clean_text!r}')
# Output: 'Hello World!'

print(repr(color_text))
# Output: '\x1b[94mHello World!\x1b[0m'

print(f'{color_text!r}')
# Output: '\x1b[94mHello World!\x1b[0m'
```

## Writing to files

When you write the colored text to a file, it will write the special characters to the file instead of the actual text.

```python
from ColorfulOutput import BLUE

clean_text = "Hello World!"
color_text = BLUE(clean_text)

with open("file.txt", "w") as file:
    file.write(clean_text)
    file.write(color_text)
```

`file.txt:`
```
Hello World!
[94mHello World![0m
```

## Length

The special characters will also be counted as characters when you use the `len()` function.

```python
from ColorfulOutput import BLUE

clean_text = "Hello World!"
color_text = BLUE(clean_text)

print(len(clean_text))
# Output: 12

print(len(color_text))
# Output: 21
```

## Adding multiple colors and styles

When you add multiple colors and styles to a string, it will not work as expected.

```python
from ColorfulOutput import BLUE, BOLD, UNDERLINE

text = BLUE("Hello ")
text += BOLD("World!")

full_text = UNDERLINE(text)

print(full_text)
```

`Console output:`  
![Console output](Images/Other/invalid_output.png)


# Workarounds

The only workaround for most of these issues is to create a "clean" string that only contains the text (as shown in the examples above).  
Then a separate "color" string that contains the text with the colors and styles.

# Future

All of these issues will be fixed in the future, but for now, you will have to use the workarounds.

If you any suggestions or issues, please let me know!
