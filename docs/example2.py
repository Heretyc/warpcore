from warpcore.engineering import WarpCore

import hashlib  # Used only for this example


def do_the_thing(number):
    hash = hashlib.pbkdf2_hmac("sha512", str.encode(f"{number}"), b"salt", 100000)


if __name__ == "__main__":
    tasks_list = []

    for number in range(0, 100):
        # Build your tasks/jobs list any way needed
        tasks_list.append(number)

    # Instance the class
    warpcore = WarpCore()

    # Equivalent to:
    # warpcore.list_engage(tasks_list, do_the_thing)
    warpcore.list_profile(tasks_list, do_the_thing)
    # Runs a trial run of your code and times performance at various iterations
    # to determine the fastest combination of settings which work for your code

    # NOTE:
    # It is preferable to limit the length of the data when profiling,
    # unless you want profiling to take all day.
