from typing import Iterable, Dict
from functools import wraps
from multiprocessing.pool import ThreadPool
import multiprocessing
import threading
import sys

"""warpcore.py: Streamlined multi-threaded process acceleration"""

__author__ = "Brandon Blackburn"
__maintainer__ = "Brandon Blackburn"
__email__ = "contact@bhax.net"
__website__ = "https://keybase.io/blackburnhax"
__copyright__ = "Copyright 2021 Brandon Blackburn"
__license__ = "Apache 2.0"

#  Copyright (c) 2021. Brandon Blackburn - https://keybase.io/blackburnhax, Apache License, Version 2.0.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
#  Unless required by applicable law or agreed to in writing,
#  software distributed under the License is distributed on an
#  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
#  either express or implied. See the License for the specific
#  language governing permissions and limitations under the License.
#  TL;DR:
#  For a human-readable & fast explanation of the Apache 2.0 license visit:  http://www.tldrlegal.com/l/apache2


class WarpCore:
    def __init__(self, max_parallel=None):
        if max_parallel is None:
            self._max_threads = multiprocessing.cpu_count()
        else:
            self._max_threads = max_parallel
        self._chunk_size = self._max_threads * 32
        self._threadLimiter = threading.BoundedSemaphore(self._max_threads)

    class _Lock:
        def __init__(self):
            self.lock = threading.Lock()

        def __enter__(self):
            self.lock.acquire()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.lock.release()

    new_lock = type(
        "lock",
        (_Lock,),
        {
            "__doc__": "A dynamic context-aware lock object suitable for multi-threaded operations."
        },
    )

    def _thread_decorator(self, func):
        @wraps(func)
        def function_wrapper(*args, **kwargs):
            self._threadLimiter.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                self._threadLimiter.release()

        setattr(sys.modules[func.__module__], func.__name__, function_wrapper)
        return function_wrapper

    def list_profile(self, *args):
        from datetime import datetime

        cpu_compute = True
        results = list()
        delta_slow = 0
        record_increase = 0
        record_threads = 0
        record_mode = cpu_compute

        def _run(cpu_compute, record_increase, record_threads, record_mode):
            for threads in range(1, (self._max_threads * 4) + 1):
                self._threadLimiter = threading.BoundedSemaphore(threads)
                if threads < 2:
                    start_slow = datetime.now()
                else:
                    start_fast = datetime.now()
                result = self.list_engage(*args, compute=cpu_compute)
                if threads < 2:
                    finish_slow = datetime.now()
                    delta_slow = finish_slow - start_slow
                    print(f"Baseline: {delta_slow.seconds} seconds")
                else:
                    finish_fast = datetime.now()

                    delta_fast = finish_fast - start_fast
                    increase = delta_slow - delta_fast
                    percent_inc = round(increase / delta_slow * 100, 1)
                    if percent_inc >= record_increase:
                        record_increase = percent_inc
                        record_threads = threads
                        record_mode = cpu_compute
                    print(
                        f"{percent_inc}% performance gain with max_parallel: {threads}"
                    )
            return record_increase, record_threads, record_mode

        record_increase, record_threads, record_mode = _run(
            True, record_increase, record_threads, record_mode
        )
        record_increase, record_threads, record_mode = _run(
            False, record_increase, record_threads, record_mode
        )

        if record_mode:
            print(
                f"RESULTS: Best performance ({record_increase}% gain) using * compute:True * with max_parallel: {record_threads}"
            )
        else:
            print(
                f"RESULTS: Best performance ({record_increase}% gain) using * compute:False (Default)* with max_parallel: {record_threads}"
            )
        exit(3)

    def dict_profile(self, *args):
        from datetime import datetime

        cpu_compute = True
        results = list()
        delta_slow = 0
        record_increase = 0
        record_threads = 0
        record_mode = cpu_compute

        def _run(cpu_compute, record_increase, record_threads, record_mode):
            for threads in range(1, (self._max_threads * 4) + 1):
                self._threadLimiter = threading.BoundedSemaphore(threads)
                if threads < 2:
                    start_slow = datetime.now()
                else:
                    start_fast = datetime.now()
                result = self.list_engage(*args, compute=cpu_compute)
                if threads < 2:
                    finish_slow = datetime.now()
                    delta_slow = finish_slow - start_slow
                    print(f"Baseline: {delta_slow.seconds} seconds")
                else:
                    finish_fast = datetime.now()

                    delta_fast = finish_fast - start_fast
                    increase = delta_slow - delta_fast
                    percent_inc = round(increase / delta_slow * 100, 1)
                    if percent_inc >= record_increase:
                        record_increase = percent_inc
                        record_threads = threads
                        record_mode = cpu_compute
                    print(
                        f"{percent_inc}% performance gain with max_parallel: {threads}"
                    )
            return record_increase, record_threads, record_mode

        record_increase, record_threads, record_mode = _run(
            True, record_increase, record_threads, record_mode
        )
        record_increase, record_threads, record_mode = _run(
            False, record_increase, record_threads, record_mode
        )

        if record_mode:
            print(
                f"RESULTS: Best performance ({record_increase}% gain) using * compute:True * with max_parallel: {record_threads}"
            )
        else:
            print(
                f"RESULTS: Best performance ({record_increase}% gain) using * compute:False (Default)* with max_parallel: {record_threads}"
            )
        exit(3)

    def list_engage(
        self, iterable: Iterable, worker_function: object, timeout=None, **kwargs
    ):
        """
        Execute a list of jobs against the worker_function
        Operates similar to-
        for item in iterable:
            worker_function(item)
        :param iterable: A list or list-like object that contains the jobs
        :param worker_function: A function that will be run in multiple threads against the jobs
        :param timeout: How many seconds to wait per thread before giving up
        :keyword compute: (bool) If True, switch to CPU compute mode. Default (False) favors I/O over CPU
        """
        worker_function = self._thread_decorator(worker_function)
        compute_intensive = kwargs.get("compute", False)
        results = list()

        if compute_intensive:
            pool = multiprocessing.Pool()
        else:
            pool = ThreadPool()
        # Generator-friendly operation, rather than just iterating over a list
        iterations = 0
        max_iterations = self._chunk_size
        threads = list()

        # Keeping generator instanced so we don't loose the current index on the generator object
        for queue_index in iterable:
            # splitting the threads into chunks to prevent loading all jobs at once and soaking resources
            if iterations >= max_iterations:
                for thread in threads:
                    results.append(thread.get(timeout))
                iterations = 0
            job = pool.apply_async(worker_function, (queue_index,))
            threads.append(job)
            iterations += 1
        # mop up any remaining threads by waiting for them to terminate
        for thread in threads:
            results.append(thread.get(timeout))
        return results

    def dict_engage(
        self, dictionary: Dict, worker_function: object, timeout=None, **kwargs
    ):
        """
        Execute a dictionary of jobs against the worker_function
        Operates similar to-
        for key, value in dictionary.items():
            worker_function(key, value)
        :param dictionary: A dict or dict-like object that contains the jobs
        :param worker_function: A function that will be run in multiple threads against the jobs
        :param timeout: How many seconds to wait per thread before giving up
        :keyword compute: (bool) If True, switch to CPU compute mode. Default (False) favors I/O over CPU
        """
        worker_function = self._thread_decorator(worker_function)
        compute_intensive = kwargs.get("compute", False)
        results = list()

        if compute_intensive:
            pool = multiprocessing.Pool()
        else:
            pool = ThreadPool()
        # Generator-friendly operation, rather than just iterating over a list
        iterations = 0
        max_iterations = self._chunk_size
        threads = list()

        # Keeping generator instanced so we don't loose the current index on the generator object
        for key, value in dictionary.items():
            # splitting the threads into chunks to prevent loading all jobs at once and soaking resources
            if iterations >= max_iterations:
                for thread in threads:
                    results.append(thread.get(timeout))
                iterations = 0
            job = pool.apply_async(worker_function, (key, value))
            threads.append(job)
            iterations += 1
        # mop up any remaining threads by waiting for them to terminate
        for thread in threads:
            results.append(thread.get(timeout))
        return results
