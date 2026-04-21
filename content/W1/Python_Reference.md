# Imperative Programming with Python

## Progrmming Environment

### Shell

- Navigation: `pwd`, `dir`/`ls`, `cd`, `.`, `..`, `~`, `-`, absolute/relative paths
- Environment Variables: `echo`, `env`, `which`/`where`, `$PATH`/`%PATH%`/`$env.PATH`

### Dependency Management

- Create a new Python virtual environment: `uv venv -p 3.11`
- Activate the environment
  - Unix: `. .venv/bin/activate`
  - Windows: `.venv\Scripts\activate`
- Install packages into the environment: `uv pip install jupyter`
- Run a script using the environment: `uv run script.py`

### IDEs

- VS Code
- JupyterLab
- Google Colab

## Python Basics

### Values

- Literals
  - NoneType: `None`
  - bool: `True`, `False`
  - int: `0`, `4`, `-2`, `1000`, `1_000_000`, `-1_02_40`, `0b101`, `0o17`, `0x1f`
  - float: `1.5`, `5.0`, `0.0`, `-1.232`, `1e6`, `1e-3`, `-2.5e-3`
  - complex: `1 + 2j`, `1.5 - 3.2j`, `1j`
  - str: `"hi"`, `'hi'`, `"""hi"""`, `'''hi'''`
- Containers: `list`, `tuple`, `set`, `dict`

### Operators

- [Documentation](https://docs.python.org/3/library/operator.html#mapping-operators-to-functions)
- [Precedence](https://docs.python.org/3/reference/expressions.html#operator-precedence)
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `//`, `**`, `@`
- Assignment: `=`, `+=`, `-=`, `*=`, `/=`, `%=`, `//=`, `**=`, `@=`, `:=`
- Comparison: `<`, `>`, `<=`, `>=`, `==`, `!=`
- Logical: `and`, `or`, `not`
- Bitwise: `&`, `|`, `^`, `~`
- Membership (used for str and containers): `in`, `not in`
- Identity (usually used for None only): `is`, `is not`
- Type Casting
  - `int("-1_02_40")`, `int(1.5)`, `float(3)`, `float("-2.5e-3")`, `complex("1+3j")`, `int("32", base=4)`
  - False: `bool()`, `bool(None)`, `bool(0)`, `bool(0.0)`, `bool(0j)`, `bool("")`, `bool([])`, `bool(())`, `bool(set())`, `bool({})`
  - True: `bool(-3)`, `bool(0.2)`, `bool(5j)`, `bool("False")`, `bool([3])`, `bool((2,))`, `bool({3})`, `bool({5: 4})`

### Control Flow

- No OP: comments, pass, or `...` (Ellipsis)
- if

```python
if grade >= 90:
    print("A")
elif grade >= 80:
    print("B")
elif grade >= 70:
    print("C")
elif grade >= 60:
    print("D")
else:
    print("F")

parity = "even" if number % 2 == 0 else "odd"
```

- match

```python
match input():
    case "0":
        print("You entered 0.")
    case "1":
        print("You entered 1.")
    case "2":
        print("You entered 2.")
    case _:
        print("You entered an invalid input.")
```

- while

```python
i = 1
while i < 10:
    if i == 3:
        print("skip 3!")
        continue
    if i == 9:
        break
    print(i)
    i += 1
else:
    print("did not encounter 9!")
```

- for

```python
for x in "abcdef":
    if x == "b":
        continue
    if x == "e":
        break
    print(x)
else:
    print("did not encounter e!")
```

- assert: `assert 4 > 2, "4 must be greater than 2"`
- try

```python
try:
    x = 1 / int(input())
except ValueError as error:
    error_message = "You didn't enter a valid number!"
    raise ValueError(error_message) from error
except ZeroDivisionError:
    print("We cannot divide by zero")
else:
    print("Done inverting the input without errors!")
finally:
    print("Goodbye!")
```

- with

```python
with open("./input.txt", mode="r") as file:
    print(file.read())

# File modes (can be combined like 'rb+')
# 'r': open for reading (default)
# 'w': open for writing, truncating the file first
# 'x': open for exclusive creation, failing if the file already exists
# 'a': open for writing, appending to the end of the file if it exists
# 'b': binary mode
# 't': text mode (default)
# '+': open a disk file for updating (reading and writing)
```

### Built-in Types

- Documentation: https://docs.python.org/3/library/stdtypes.html
- str (immutable)
  - Escape Characters:
    - backslash: `\\`
    - single quote: `\'`
    - double quote: `\"`
    - new line: `\n`
    - ingored character: `\<newline>`
    - new tab: `\t`
    - backspace: `\b`
    - carriage return: `\r`
    - hex character: `\x5a`
    - unicode character: `\u0623`
  - Operations
    - Indexing and Slicing: similar to list
    - Concatenate: `"abc" + "def"`
    - Concatenate: `"abc" "def"`
    - Repeat: `"abc" * 4`
    - Contains: `"b" in "abc"`
    - Loop: `for x in "abc": print(x)`
  - Methods
    - Case: upper, lower, title, capitalize, swapcase, casefold
    - split, rsplit, splitlines, join, partition, rpartition
    - Check: startswith, endswith, isnumeric, isdecimal, isdigit, isalpha, isalnum, isascii, isidentifier, isprintable, isspace, islower, isupper, istitle
    - Search: find, rfind, index, rindex, count
    - Replace: replace, expandtabs, format, format_map
    - Clean: removeprefix, removesuffix, strip, lstrip, rstrip
    - Organize: center, just, ljust, rjust, zfill
    - Represent: encode, translate, maketrans
  - Types
    - raw strings `r"C:\Users\User\Desktop"`
    - bytes strings `b"\x32\x8b"`
    - format strings `f"resutt = {x}"`
    - unicode strings `u"hi"` (default)
  - Formatting
    - [Documentation](https://docs.python.org/3/library/string.html)
    - printf-style `"The value of %s is %d" % ("x", 4)`
    - template strings
    - format specification
      - fill: any character to fill the empty spaces
      - align: where should the value be aligned `<` (left), `^` (center), or `>` (right)
      - sign: `-` (only show the sign if the number is negative), `+` (also show the sign for positive numbers), or ` ` (keep an empty space in the place of the sign for positive numbers)
      - 0: fill zeros if applicable
      - width: the total width of the value
      - grouping: to group every three digits of the number `,` or `_`
      - type: `d` (for integers) or `.3f` (for floating point numbers along with the precision)
      - Example: `f"Result = {5 / 3:$^+9,.2f}"` gives `Result = $$+1.67$$`
- list (mutable)
  - Examples
    - `[1, 2, 3, 4]`
    - `[1, 2, 3, 4,]`
    - `[1, "b", 4]`
    - `[]`
    - `list()`
  - Methods
    - Add: append, insert, extend
    - Remove: pop, remove, clear
    - Search: index, count
    - Order: reverse, sort, copy
  - Operations: `x = [4, 5, 6, 7, 8, 9]`
    - Indexing
      - `x[1]`
      - `x[-2]`
      - `x[0]`
    - Slicing
      - `x[1:3]`
      - `x[0:-2]`
      - `x[-3:]`
      - `x[::2]`
      - `x[:]`
      - `x[None:None]`
      - `x[1::2]`
      - `x[::-1]`
      - `x[slice(1, 3, None)]`
    - Deleting Elements
      - `del x[1]`
      - `del x[:2]`
    - Editing Elements
      - `x[3] = 1`
      - `x[1:3] = [1, 2]`
      - `x[1:3] = [1, 2, 3, 4, 5]`
    - Loop: `for e in x: print(e)`
    - Comprehension
      - `[e for e in [1, 2, 3] if e > 0]`
      - `[e for l in [[1, 2], [3, 4], [5, 6, 7]] for e in l]`
      - `[e for l in [[1, 2], [3, 4], [5, 6, 7]] if len(l) < 3 for e in l if e > 1]`
    - Packing
      - `a, b, *c = [1, 2, 3, 4]`
      - `a, *b, c = [1, 2, 3, 4]`
      - `*a, b = [1, 2, 3, 4]`
      - `a, *b = (1, 2, 3, 4)`
    - Unpacking: `[1, 2, *[3, 4, 5], 6]`
- tuple (immutable)
  - Examples
    - `(1, 2, 3)`
    - `(1, 2, 3,)`
    - `1, 2, 3`
    - `(2,)`
    - `5,`
    - `()`
    - `tuple()`
  - Methods: count, index
  - Operations: `x = (1, 2, 3, 4)`
    - Indexing and Slicing: similar to list
    - Loop: `for e in x: print(e)`
    - Comprehension: `tuple(e for e in x if e > 0)`
    - Unpacking
      - `[1, 2, *(3, 4, 5), 6]`
      - `(*(1, 2, 3),)`
      - `a, b = 1, 2`
- set (mutable)
  - Examples
    - `{1, 2, 3}`
    - `{1, 2, 3, 3, 2,}`
    - `{3}`
    - `set()`
  - Methods
    - Other: add, copy
    - Remove: pop, remove, discard, clear
    - Check: isdisjoint, issubset, issuperset
    - Operate: union, intersection, difference, symmetric_difference
    - Update: update, intersection_update, difference_update, symmetric_difference_update
  - Operations: `x = {1, 2, 3, 4, 5}`
    - Loop: `for e in x: print(e)`
    - Comprehension: `{e for e in x if e > 0}`
    - Unpacking: `[1, 2, *{3, 4, 5}, 6]`
- dict (mutable)
  - Examples
    - `{"a": 1, "bc": 2, "def": 3}`
    - `{1: 2, 2: 4, 3: 6}`
    - `{1: 2, "2": 4, "cd": 6}`
    - `{}`
    - `dict()`
    - `dict.fromkeys(["a", "b", "c"])`
  - Methods
    - Iterators: keys, values, items
    - Access: get, pop, popitem, setdefault, update, clear, copy
  - Operations: `x = {"a": 1, "b": 2, "c": 3}`
    - Element Access: `x["a"]`
    - Deleting Elements: `del x["b"]`
    - Loop
      - `for k in x.keys(): print(k)`
      - `for v in x.values(): print(v)`
      - `for k, v in x.items(): print(k, v)`
      - `for k in x: print(k)`
    - Comprehension: `{k: 2 * v for k, v in x.items() if k.lower()}`
    - Unpacking
      - `{"a": 7, **x, "m": 8}`
      - `{**x, "a": 7, "m": 8}`

## Procedural Programming

### Functions

- positional and keyword arguments

```python
def add(a: float, b: float = 1.0) -> float:
    return a + b

print(add(1, 2))
print(add(7))
print(add(a=1, b=2))
print(add(b=2, a=1))
```

- variadic argument (tuple)

```python
def accumulate(*numbers: float) -> float:
    total = 0
    for number in numbers:
        total += number
    return total

print(accumulate(1, 2, 3, 4, 5, 6))
```

- variadic argument (dict)

```python
def double(**values: float) -> dict[str, float]:
    for key, value in values.items():
        values[key] = value * 2
    return values

print(double(a=1, b=2))
```

- positional/keyword-only arguments

```python
# a: positional-only argument
# b: positional-or-keyword argument
# c: keyword-only argument
def f(a, /, b, *, c):
    print(a, b, c)

f(1, 2, c=3)
f(1, b=2, c=3)
f(1, c=3, b=2)
```

- lambda

```python
list(map(lambda x: x**2 - 1, [1, 2, 3, 4]))
list(filter(lambda x: x % 2 == 0, [1, 2, 3, 4]))
```

- recursion

```python
def count_down(n: int) -> None:
    if n < 0:
        return None
    print(n)
    count_down(n - 1)

count_down(10)
```

- closures

```python
def print_lines(lines: list[str]):
    def print_line(line: str) -> None:
        nonlocal i
        print(f"{i:>3}: {line}")
        i += 1

    i = 0
    for line in lines:
        print_line("v" * 10)
        print_line(line)
        print_line("^" * 10)

print_lines(['a', 'b', 'c'])
```

- global

```python
def f():
    global x
    x += 1
    print(x)

x = 0
f()
```

- generators

```python
def counter():
    print('a')
    yield 1
    print('b')
    yield 2
    print('c')
    yield 3
    print('d')

for x in counter():
    print(x)
```

- decorators

```python
def logged(function):
    def wrapper(*args, **kwargs):
        print(f"Calling: {function.__name__}()...")
        return function(*args, **kwargs)
    return wrapper

@logged
def add(a, b):
    return a + b

add(1, 2)
```

### Built-in Functions

- [Documentation](https://docs.python.org/3/library/functions.html)
- I/O: input, print, open
- Math: abs, pow, round, divmod
- Sequence Math: len, sum, max, min, all, any
- Sequence Manipulation: reversed, sorted, enumerate, zip, map, filter, slice
- Iterators: range, iter, next, aiter, anext
- Identity: type, help, id, hash, callable, isinstance, issubclass
- Types: bool, int, float, complex, list, tuple, set, frozenset, dict
- Binary: bytes, bytearray (mutable), memoryview
- Representation: str, repr, ascii, format, ord, chr, bin, oct, hex
- Inspection: dir, vars, hasattr, getattr, setattr, delattr, locals, globals
- Debugging: breakpoint, eval, exec, compile

## Object-Oriented Programming

- Encapsulation

```python
class Person:
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age  # will check if the age is valid

    @property
    def age(self) -> int:
        return self._age

    @age.setter
    def age(self, value: int) -> None:
        assert 0 <= value <= 200, f"`{value}` is not a valid age!"
        self._age = value

    @age.deleter
    def age(self) -> None:
        self._age = 0

    @property
    def first_name(self) -> str:
        return self.name.split(" ")[0]

    @property
    def last_name(self) -> str:
        return self.name.split(" ")[-1]

    def get_card(self, header: str = "@", footer: str = "^") -> str:
        line = f"| {self.name} ({self.age}) |"
        return f"{header * len(line)}\n{line}\n{footer * len(line)}"

    def __eq__(self, other) -> bool:
        return self.name == other.name and self.age == other.age

    def __repr__(self) -> str:
        return f"Person(name='{self.name}', age={self.age})"
```

- Inheritence

```python
class Employee(Person):
    def __init__(self, name: str, age: int, salary: float) -> None:
        super().__init__(name, age)
        self.salary = salary

class Student(Person):
    def __init__(self, name: str, age: int, grades: list[float]) -> None:
        super().__init__(name, age)
        self.grades = grades

    @property
    def average(self) -> float:
        return sum(self.grades) / len(self.grades)

class WorkingStudent(Employee, Student):
    def __init__(self, name, age, salary, grades):
        self.name = name
        self.age = age
        self.salary = salary
        self.grades = grades
```

- Polymorphism

```python
values = ["abc", ["c", "b", "b"], ("a", "b", "a")]

for value in values:
    print(value.count("a"))
```

## Modules and Packages

### Built-in Modules

- [Documentation](https://docs.python.org/3/py-modindex.html)
- System
  - os: environ, getcwd, chdir, mkdir, rename, remove
  - sys: path, argv, stdin, stdout, stderr
  - time: sleep, time, perf_counter_ns, strftime
  - shutil: copyfileobj, copytree, move, rmtree, which
- Utilities: math, random, itertools, functools, typing, timeit
- Files

  - pathlib.Path: home, touch, mkdir, symlink_to, glob, iterdir, exists, is_dir, is_file, expanduser, parent, parts, name, stem, suffix
  - json

  ```python
  import json

  print(json.dumps({"name": "Ward", "male": False, "age": 3}))
  print(json.loads("[false, null]"))
  ```

  - csv

  ```python
  import csv

  with open("data.csv", "w") as file:
     writer = csv.writer(file)
     writer.writerow(["A", "B", "C"])
     writer.writerow([1, 2, 3])
     writer.writerow([4, 5, 6])

  with open("data.csv") as file:
     for row in csv.DictReader(file):
        print(row)
  ```

  - base64

  ```python
  from base64 import b64encode, b64decode

  encoded = b64encode("hi".encode())
  print("base64:", encoded.decode())
  print("value :", b64decode(encoded).decode())
  ```

  - pickle

  ```python
  import pickle

  with open("data.pkl", "wb") as file:
     pickle.dump({"name": "Ward", "male": False, "age": 3}, file)

  data = pickle.load(open("data.pkl", "rb"))
  ```

### Custom Modules

```plaintext
src/
├── utilities/
│   ├── arithmetic/
│   │   ├── operations.py
│   │   └── units.py
│   └── validation.py
└── main.py
```

```python
# main.py
import utilities.arithmetic.units as convert
from utilities.arithmetic.operations import add
from utilities.validation import *

def main():
    fahrenheit = input_float("F: ")
    celsius = convert.temperature(add(fahrenheit, 20), "F")
    print("C:", celsius)

if __name__ == "__main__":
    main()
```

```python
# utilities/validation.py
def input_float(prompt: str = "") -> float:
    while True:
        try:
            x = input(prompt)
            return float(x)
        except ValueError:
            print(f"You entered `{x}` which is not a number. Please, enter a valid number.")
```

```python
# utilities/arithmetic/operations.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b
```

```python
# utilities/arithmetic/units.py
def temperature(value, src, dst="C"):
    assert src in "CKF", f"Unknown source unit `{src}`"
    assert dst in "CKF", f"Unknown output unit `{dst}`"
    match src:
        case "K":
            value -= 273.15
        case "F":
            value = (value - 32) / 1.8
    match dst:
        case "K":
            value += 273.15
        case "F":
            value = value * 1.8 + 32
    return value
```

### 3rd Party Packages

- UI: typer and streamlit (textual, customtkinter, flet, gradio)
- API: httpx/requests and fastapi

### typer

Create feature-rich CLI based on type Python type hints. Learn more about typer's advanced fetures [here](https://typer.tiangolo.com/tutorial/).

#### Install

```bash
uv pip install typer
```

#### Usage

```python
import typer

app = typer.Typer()


@app.command()
def hello(name: str):
    print(f"Hello {name}")


@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
```

Then:

```bash
uv run main.py --help
```

### httpx

A fully-features HTTP client for Python.

#### Install

```bash
uv pip install httpx
```

#### Usage

```python
import httpx

r = httpx.get('https://httpbin.org/get')
print(r.text)  # r.content (binary) or r.json()

with httpx.Client() as client:
    r = client.get('https://example.com')

r = httpx.put('https://httpbin.org/put', data={'key': 'value'})
r = httpx.delete('https://httpbin.org/delete')
r = httpx.head('https://httpbin.org/get')
r = httpx.options('https://httpbin.org/get')
```

### fastapi

A powerful yet simple framework to create RESTful APIs.

#### Install

```bash
uv pip install "fastapi[standard]"
```

#### Usage

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
```

Then:

```bash
fastapi dev main.py
```
