import shepherd
import unittest
import example
from multiprocessing import Pool



def run_example():
  return shepherd.run_server(example.datasource, example.mapfn, example.reducefn)



class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_example(self):

        expected = {'a': 2, 'on': 1, 'great': 1, 'Humpty': 3, 'again': 1, 'wall': 1, 'Dumpty': 2, 'men': 1, 'had': 1, 'all': 1, 'together': 1, "King's": 2, 'horses': 1, 'All': 1, "Couldn't": 1, 'fall': 1, 'and': 1, 'the': 2, 'put': 1, 'sat': 1}

        pool = Pool(processes=1)
        process = pool.apply_async(run_example)
        shepherd.run_clients()
        result = process.get()

        self.assertEqual(expected, result)




if __name__ == '__main__':
    unittest.main()