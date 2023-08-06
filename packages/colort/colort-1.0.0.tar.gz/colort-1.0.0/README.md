<h1 align="center">Colort</h1>

<p align="center">
    <a href="https://pepy.tech/project/colort"><img alt="Downloads" src="https://static.pepy.tech/badge/colort"></a>    
    <a href="https://pepy.tech/project/colort"><img alt="Downloads" src="https://static.pepy.tech/badge/colort/month"></a>
    <a href="https://pepy.tech/project/colort"><img alt="Downloads" src="https://static.pepy.tech/badge/colort/week"></a>
</p>

This module provides functions for formatting text with ANSI escape codes to add color and style.

## Installation

```shell
pip install colort
```

## Usage

```python
from colort import colorize
```

The `colorize` function takes a string and any number of `Style` and `*Color` enums. It returns the string formatted with the specified styles.

For example:

```python
from colorformat import colorize, ForegroundColor as fc, Style

colored_text = colorize('Hello World!', fc.GREEN, Style.BOLD)
print("colored text: ", colored_text)
```

This will print the text in bold and green.

![截屏2023-08-06 11.03.47](https://s1.ax1x.com/2023/08/06/pPANNxs.png)

The available formatting options are:

### Colors

- ForegroundColor
  - BLACK, RED, GREEN, YELLOW, BLUE, etc.
- BackgroundColor
  - BLACK, RED, GREEN, YELLOW, BLUE, etc.

### Styles

- Style
  - NORMAL, BOLD, UNDERLINE, BLINK, INVERT, HIDE

Multiple styles can be combined:

```python
colorize('Text', ForegroundColor.WHITE, BackgroundColor.RED, Style.BOLD)
```

