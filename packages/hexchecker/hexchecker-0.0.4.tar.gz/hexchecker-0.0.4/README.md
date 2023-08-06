# ✅ hexchecker

Simple Python package to check if string is valid hexadecimal.  

## 🚀 Usage

```python
from hexchecker import hexchecker, hexcheckerUpper, hexcheckerLower

# Check invalid hexadecimal
hexchecker('abcg7') # Returns False

# Check valid hexadecimal
hexchecker('aBcDeF1234567890') # Returns True

# Check valid hexidecimal, ensuring that it is in uppercase
hexcheckerUpper('ABCDEF') # Returns True
hexcheckerUpper('abcdef') # Returns False

# Check valid hexidecimal, ensuring that it is in lowercase
hexcheckerLower('abcdef') # Returns True
hexcheckerLower('ABCDEF') # Returns False
```

## 📦 Installation

Run the following to install:  

```bash
$ pip install hexchecker
```

## 👨‍💻 Developing hexchecker

To install hexchecker, along with the tools you will need to develop and run tests, run the following in your virtualenv:  

```bash
$ pip install -e .[dev]
```

## 🚦 Development Progress

Stable Development