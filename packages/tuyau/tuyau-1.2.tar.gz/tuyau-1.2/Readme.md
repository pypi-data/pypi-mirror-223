# Tuyau

[![Version](https://img.shields.io/badge/version-1.2-blue.svg)](https://github.com/guiforge/tuyau)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Tuyau is a library that allows you to process values through a sequence of steps, similar to a pipe.

```python
# Before 
for name in names:
    len(hash(upper_case(decode(name))))

# After
tube = Tube(decode, upper_case, hash, len)

for name in names:
    tube(name)

# or alternative
tube.send(name)
```

## Installation

You can install Tuyau using pip:

```bash
pip install tuyau
```

## Usage

### Creating a Tuyau

To create a Tuyau, you can pass a sequence of callable steps to the constructor. Each step should be a callable that takes one argument and returns a value of any type.

```python
from tuyau import Tube

def add_one(number: int) -> int:
    """Simple step: add one to the number."""
    return number + 1

def multiply_by_two(number: int) -> int:
    """Simple step: multiply the number by two."""
    return number * 2

tube = Tube(add_one, multiply_by_two)
print(tube.send(1)) # 4
```

### Processing Values

You can process values through the Tuyau by calling it as if it were a function. The value will go through each step in the sequence and get transformed accordingly.

```python
result = tube(5)
print(result)  # Output: 12 (5 + 1 = 6, 6 * 2 = 12)
```

You can also use the `send()` method, which is an alias for calling the Tuyau directly.

```python
result = tube.send(5)
print(result)  # Output: 12
```

### Example

Here's an example using lambda functions as steps:

```python
tube = Tube(lambda x: x + 1, lambda x: x * 2)

result = tube(3)
print(result)  # Output: 8 (3 + 1 = 4, 4 * 2 = 8)
```
## Typing
## Typing

The `Tube` class is designed to support typing for both input and output. 

```python
from tuyau import Tube

def add_one(num: int) -> int:
    return num + 1

def multiply_by_two(num: int) -> int:
    return num * 2

# Create Tube with multiple callables that take and return int
tube: Tube[int, int] = Tube(add_one, multiply_by_two)
tube: Tube[int, str] = Tube(add_one, multiply_by_two, str)

# Process integers through the tubes
result: int = tube(3)# Output: 6 (3 + 1 * 2) 
result2: str = tube(3)# Output: "6" str(3 + 1 * 2) 
```

## Contributing

Contributions are welcome! If you find a bug or have a suggestion for improvement, please create an issue or a pull request on [GitHub](https://github.com/guiforge/tuyau).

### Local dev
install .venv with all dev dep  
`make dev-install`  

launch tests  
`make test`

launch linters  
`make lint`

## License

This library is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
