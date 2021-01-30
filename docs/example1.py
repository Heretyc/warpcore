from warpcore.engineering import WarpCore
import threading  # Needed if you intend to lock for writing to shared resources

import hashlib  # Used only for this example
from datetime import datetime  # Used only for this example


def do_the_thing(number):
    # This is just an example of a function that needs to be executed as fast as possible in parallel
    print(f"Thread {number}")
    hash = hashlib.pbkdf2_hmac("sha512", str.encode(f"{number}"), b"salt", 100000)

    lock.acquire()  # Wait for, and prevent execution beyond this point for any other threads
    result_list.append(hash)
    lock.release()  # Let the other threads know it's safe for the next to write

    # Alternatively, use Try:Finally clause to ensure the lock.release() always happens
    """
    lock.acquire()
    try:
        result_list.append(hash)
    finally:
        lock.release()
    """


if __name__ == "__main__":
    # Someplace to store results, we will use threading.Lock() -> lock.acquire()
    result_list = []
    # Build a task list
    tasks_list = []

    # Build the lock
    lock = threading.Lock()

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
    result_list = []
    start_fast = datetime.now()

    # Example of the same function call after WarpCore optimization
    warpcore.list_engage(tasks_list, do_the_thing)

    finish_fast = datetime.now()

    # Just calculating the percent increase in speed
    delta_slow = finish_slow - start_slow
    delta_fast = finish_fast - start_fast
    increase = delta_slow - delta_fast
    percent_inc = round(increase / delta_slow * 100, 1)

    print(f"\n{len(result_list)} Results found")
    print(f"{percent_inc}% increase with WarpCore\n")
