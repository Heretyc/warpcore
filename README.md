[![WarpCore logo](https://github.com/BlackburnHax/warpcore/raw/main/docs/warpcore.png)](https://github.com/BlackburnHax/warpcore)
# warpcore
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![pypi](https://img.shields.io/pypi/v/warpcore.svg)](https://pypi.org/project/warpcore/) [![wheel](https://img.shields.io/pypi/wheel/warpcore.svg)](https://pypi.org/project/warpcore/)
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

### Fine Tuning for Performance
_TL;DR: [example2.py](https://github.com/BlackburnHax/warpcore/blob/main/docs/example2.py) Is a working sample of the profiling system._

Your workload and processor architecture will dictate which settings work best for any situation.

You can leave things at default, but if you want to squeeze even more performance out, consider using the profiling feature.
```python
# Regular operation
warpcore.list_engage(tasks_list, do_the_thing)

# Performance Profiling mode of same function as above
warpcore.list_profile(tasks_list, do_the_thing)
```
Profiling simply runs your code, but benchmarks execution time of the full job list. Then tweaks the settings and re-runs the jobs again.

Each time it re-runs, it displays the performance metrics of the last run on console.

Once complete, it will display the suggested combination of settings
#### Example 1
```shell
RESULTS: Best performance (85.8% gain) using * compute:True * with max_parallel: 51
```
This translates to the following setup:
```python
warpcore = WarpCore(51)
warpcore.list_engage(tasks_list, do_the_thing, compute=True)
```
#### Example 2
```shell
RESULTS: Best performance (91.4% gain) using * compute:False (Default)* with max_parallel: 32
```
This translates to the following setup:
```python
warpcore = WarpCore(32)
warpcore.list_engage(tasks_list, do_the_thing, compute=False)
# or just leave out 'compute' keyword to assume False
warpcore.list_engage(tasks_list, do_the_thing)
```

## Meta

Brandon Blackburn – [PGP Encrypted Chat @ Keybase](https://keybase.io/blackburnhax/chat)

Distributed under the Apache 2.0 license. See ``LICENSE`` for more information.

_TL;DR:_
For a human-readable & fast explanation of the Apache 2.0 license visit:  http://www.tldrlegal.com/l/apache2


[https://github.com/BlackburnHax/warpcore](https://github.com/BlackburnHax/warpcore)