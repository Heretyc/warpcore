[![WarpCore logo](https://github.com/BlackburnHax/warpcore/raw/main/docs/warpcore.png)](https://github.com/BlackburnHax/warpcore)
# warpcore
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
> Streamlined multi-threaded process acceleration

When working with software that needs to be performant, it’s challenging to deal with all the pitfalls of multi-threading while balancing code stability.

Smoothing out the bumps in the road to multi-threading is the primary goal of the project. It’s just that simple.


## Installation

OS X, Linux & Windows:

```sh
pip install warpcore
```


## Usage Examples

### List Operations
1. Build a list of arguments that will be passed to a designated function.
```python
jobs = []
jobs.append("Picard")
jobs.append("Janeway")
jobs.append("Kirk")
jobs.append("Sisko")
jobs.append("Archer")
```
2. Create a function that will iterate over the list:
```python
def do_the_thing(name):
    print(f"Star Fleet Captain {name}")
```
3. Create a single-threaded version to test:
```python
for name in jobs:
    do_the_thing(name)
```
4. Once that works, convert the for-loop into a warpcore call
```python
warpcore.list_engage(jobs, do_the_thing)
```

Full example:
```python
from warpcore.engineering import WarpCore

def do_the_thing(name):
    print(f"Star Fleet Captain {name}")

jobs = []
jobs.append("Picard")
jobs.append("Janeway")
jobs.append("Kirk")
jobs.append("Sisko")
jobs.append("Archer")

# Single-threaded operation (for testing/debug)
# for name in jobs:
#     do_the_thing(name)

# Multi-threaded operation (for normal operation)
warpcore = WarpCore()
warpcore.list_engage(jobs, do_the_thing)
```
Please refer to [example0.py](https://github.com/BlackburnHax/warpcore/blob/main/docs/example0.py) and [example1.py](https://github.com/BlackburnHax/warpcore/blob/main/docs/example1.py) for basic and more advanced usage examples respectively.

### Dictionary Operations
1. Build a dict of arguments that will be passed to a designated function.
```python
database = {
    "Picard": "USS Enterprise-D",
    "Janeway": "USS Voyager",
    "Kirk": "USS Enterprise-A",
    "Sisko": "Deep Space 9",
    "Archer": "Enterprise NX-01"
}
```
2. Create a function that will iterate over the dictionary:
#### *Note when using dicts, make sure your worker function accepts the `key` and `value` as arguments. (See below)
```python
def do_the_thing(key, value):
    print(f"Star Fleet Captain {key} is/was in command of {value}")
```
3. Create a single-threaded version to test:
```python
for key, value in database.items():
    do_the_thing(key, value)
```
4. Once that works, convert the for-loop into a warpcore call
```python
warpcore.dict_engage(database, do_the_thing)
```

Full example:
```python
from warpcore.engineering import WarpCore

def do_the_thing(key, value):
    print(f"Star Fleet Captain {key} is/was in command of {value}")

database = {
    "Picard": "USS Enterprise-D",
    "Janeway": "USS Voyager",
    "Kirk": "USS Enterprise-A",
    "Sisko": "Deep Space 9",
    "Archer": "Enterprise NX-01"
}

# Single-threaded operation (for testing/debug)
# for key, value in database.items():
#     do_the_thing(key, value)

# Multi-threaded operation (for normal operation)
warpcore = WarpCore()
warpcore.dict_engage(jobs, do_the_thing)
```
## Meta

Brandon Blackburn – [PGP Encrypted Chat @ Keybase](https://keybase.io/blackburnhax/chat)

Distributed under the Apache 2.0 license. See ``LICENSE`` for more information.

_TL;DR:_
For a human-readable & fast explanation of the Apache 2.0 license visit:  http://www.tldrlegal.com/l/apache2


[https://github.com/BlackburnHax/warpcore](https://github.com/BlackburnHax/warpcore)