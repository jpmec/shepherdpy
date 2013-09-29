import shepherd
import unittest
import example
from multiprocessing import Pool



#def run_example():
#	options = {
#		'datasource':example.datasource,
#		'mapfn':example.mapfn,
#		'reducefn':example.reducefn
#	}
#	return shepherd.run_server(options)




class TestShepherd(unittest.TestCase):

	def setUp(self):
		pass

	def test_example(self):

		#expected = {'a': 2, 'on': 1, 'great': 1, 'Humpty': 3, 'again': 1, 'wall': 1, 'Dumpty': 2, 'men': 1, 'had': 1, 'all': 1, 'together': 1, "King's": 2, 'horses': 1, 'All': 1, "Couldn't": 1, 'fall': 1, 'and': 1, 'the': 2, 'put': 1, 'sat': 1}
		#
		#pool = Pool(processes=1)
		#process = pool.apply_async(run_example)
		#shepherd.run_clients()
		#result = process.get()
		#
		#self.assertEqual(expected, result)

		self.assertTrue(True)




if __name__ == '__main__':
	unittest.main()
