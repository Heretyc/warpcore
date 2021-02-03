from typing import Iterable, Dict
from multiprocessing import cpu_count
import threading
import inspect

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
    def __init__(self):
        self._max_threads = cpu_count()
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
        def function_wrapper(*args, **kwargs):
            self._threadLimiter.acquire()
            try:
                return func(*args, **kwargs)
            finally:
                self._threadLimiter.release()

        return function_wrapper

    def list_engage(self, iterable: Iterable, worker_function: object, timeout=None):
        """
        Execute a list of jobs against the worker_function
        Operates similar to-
        for item in iterable:
            worker_function(item)
        :param iterable: A list or list-like object that contains the jobs
        :param worker_function: A function that will be run in multiple threads against the jobs
        :param timeout: How many seconds to wait per thread before giving up
        """
        worker_function = self._thread_decorator(worker_function)

        # Generator-friendly operation, rather than just iterating over a list
        iterations = 0
        max_iterations = self._chunk_size
        threads = list()
        # Keeping generator instanced so we don't loose the current index on the generator object
        for queue_index in iterable:
            # splitting the threads into chunks to prevent loading all jobs at once and soaking resources
            if iterations >= max_iterations:
                for index, thread in enumerate(threads):
                    thread.join(timeout=timeout)
                    while thread.is_alive():
                        pass
                iterations = 0
            job = threading.Thread(target=worker_function, args=(queue_index,))
            threads.append(job)
            job.start()
            iterations += 1
        # mop up any remaining threads by waiting for them to terminate
        for index, thread in enumerate(threads):
            thread.join(timeout=timeout)
            while thread.is_alive():
                pass

    def dict_engage(self, dictionary: Dict, worker_function: object, timeout=None):
        """
        Execute a dictionary of jobs against the worker_function
        Operates similar to-
        for key, value in dictionary.items():
            worker_function(key, value)
        :param dictionary: A dict or dict-like object that contains the jobs
        :param worker_function: A function that will be run in multiple threads against the jobs
        :param timeout: How many seconds to wait per thread before giving up
        """
        worker_function = self._thread_decorator(worker_function)

        # Generator-friendly operation, rather than just iterating over a list
        iterations = 0
        max_iterations = self._chunk_size
        threads = list()
        # Keeping generator instanced so we don't loose the current index on the generator object
        for key, value in dictionary.items():
            # splitting the threads into chunks to prevent loading all jobs at once and soaking resources
            if iterations >= max_iterations:
                for index, thread in enumerate(threads):
                    thread.join(timeout=timeout)
                    while thread.is_alive():
                        pass
                iterations = 0
            job = threading.Thread(target=worker_function, args=(key, value))
            threads.append(job)
            job.start()
            iterations += 1
        # mop up any remaining threads by waiting for them to terminate
        for index, thread in enumerate(threads):
            thread.join(timeout=timeout)
            while thread.is_alive():
                pass
