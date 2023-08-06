# parol

[![PyPI](https://img.shields.io/pypi/v/parol)](https://pypi.org/project/parol/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parol)](https://www.python.org/downloads/)
[![GitHub last commit](https://img.shields.io/github/last-commit/daxartio/parol)](https://github.com/daxartio/parol)
[![GitHub stars](https://img.shields.io/github/stars/daxartio/parol?style=social)](https://github.com/daxartio/parol)

## Installation

```
pip install parol
```

## Usage

```python
>>> import parol
>>> pwd = parol.generate()
>>> parol.validate(pwd.password, pwd.salt, pwd.hash)
True

```

## License

* [MIT LICENSE](LICENSE)

## Contribution

[Contribution guidelines for this project](CONTRIBUTING.md)
