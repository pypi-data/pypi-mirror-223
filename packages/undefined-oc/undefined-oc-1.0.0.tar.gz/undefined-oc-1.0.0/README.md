# undefined by Ouroboros Coding

[![pypi version](https://img.shields.io/pypi/v/undefined-oc.svg)](https://pypi.org/project/undefined-oc) ![MIT License](https://img.shields.io/pypi/l/undefined-oc.svg)

undefined: A value to use as a default value to indicate an argument was absolutely not set buy the user of the method. Will not match as true to any
other value but itself.

## Installation
```bash
pip install undefined-oc
```

## Import
```python
import undefined

def print_me(value = undefined):
  if value is undefined:
    print('Please pass a value to print')
  else:
    print(value)
```

```
>>> print_me('hello, there')
hello, there
>>> print_me(None)
None
>>> print_me([])
[]
>>> print_me()
Please pass a value to print
```