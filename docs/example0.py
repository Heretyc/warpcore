from warpcore.engineering import WarpCore
import hashlib  # Used only for this example
from datetime import datetime  # Used only for this example


def do_the_thing(number):
    # This is just an example of a function that needs to be executed as fast as possible in parallel
    print(
        f"Thread {number}  {hashlib.pbkdf2_hmac('sha512', str.encode(f'{number}'), b'salt', 100000)[:5]}"
    )
    # I personally prefer to use Class variables to store output of threads, but any thread-safe methods work
    # Be aware that WRITING to the same variable from inside a thread can cause race conditions
    # Better to also utilize threading.Lock() before writing to it first, see example1.py


if __name__ == "__main__":
    # Build a task list
    tasks_list = []

    for number in range(0, 100):
        # Build your tasks/jobs list any way needed
        tasks_list.append(number)

    # Instance the class
    warpcore = WarpCore()

    start_slow = datetime.now()
    # Example of a function call before WarpCore optimization
    for number in tasks_list:
        do_the_thing(number)

    finish_slow = datetime.now()
    start_fast = datetime.now()

    # Example of the same function call after WarpCore optimization
    warpcore.list_engage(tasks_list, do_the_thing)

    finish_fast = datetime.now()

    # Just calculating the percent increase in speed
    delta_slow = finish_slow - start_slow
    delta_fast = finish_fast - start_fast
    increase = delta_slow - delta_fast
    percent_inc = round(increase / delta_slow * 100, 1)

    print(f"\n{percent_inc}% increase with WarpCore\n")
