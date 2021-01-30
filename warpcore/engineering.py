from typing import Iterable, Dict
from multiprocessing import cpu_count
import threading

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

    @staticmethod
    def _chunker(iterable, chunk_size):
        if isinstance(iterable, list):
            for item in range(0, len(iterable), chunk_size):
                yield iterable[item : item + chunk_size]

        elif isinstance(iterable, dict):
            iteration = 0
            final_dict = {}
            for key, value in iterable.items():
                if iteration < chunk_size:
                    final_dict[key] = value
                    iteration += 1
                else:
                    yield final_dict
                    final_dict = {}
                    final_dict[key] = value
                    iteration = 0

    def list_engage(self, iterable: Iterable, worker_function: object, timeout=None):

        worker_function = self._thread_decorator(worker_function)
        for chunk in self._chunker(iterable, self._chunk_size):
            for index in chunk:
                threads = list()
                job = threading.Thread(target=worker_function, args=(index,))
                threads.append(job)
                job.start()
            for index, thread in enumerate(threads):
                thread.join(timeout=timeout)
                while thread.is_alive():
                    pass

    def dict_engage(self, dictionary: Dict, worker_function: object, timeout=None):

        worker_function = self._thread_decorator(worker_function)
        for chunk_item in self._chunker(dictionary, self._chunk_size):
            threads = list()
            for key, value in chunk_item.items():
                job = threading.Thread(target=worker_function, args=(key, value))
                threads.append(job)
                job.start()
            for index, thread in enumerate(threads):
                thread.join(timeout=timeout)
                while thread.is_alive():
                    pass
