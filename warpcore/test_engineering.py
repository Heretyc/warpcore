from unittest import TestCase
from warpcore.engineering import WarpCore


class TestWarpCore(TestCase):
    def setUp(self):
        self.warpcore = WarpCore()

    def test__thread_decorator(self):
        def test_func():
            pass

        new_func = self.warpcore._thread_decorator(test_func)
        self.assertTrue(hasattr(new_func, "__wrapped__"))

    def test_list_engage(self):
        jobs = list()

        def worker(index):
            return index + 10

        for index in range(0, 100):
            jobs.append(index)
        results = self.warpcore.list_engage(jobs, worker)

        jobs_index = 0
        for index in results:
            self.assertTrue(index == (jobs[jobs_index] + 10))
            jobs_index += 1

    def test_dict_engage(self):
        keys = []
        values = []
        jobs = {}

        def dictionary_worker(key, value):
            return key * value + 10

        for index in range(0, 100):
            keys.append(index)
            values.append(index * 2)

        for index in range(0, 100):
            jobs[keys[index]] = values[index]
        results = self.warpcore.dict_engage(jobs, dictionary_worker)
        jobs_index = 0
        for index in results:
            self.assertTrue(index == (keys[jobs_index] * (keys[jobs_index] * 2) + 10))
            jobs_index += 1
