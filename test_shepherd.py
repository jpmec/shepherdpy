import shepherd
import unittest
import example
from multiprocessing import Pool




class TestShepherd(unittest.TestCase):

	def setUp(self):
		pass


	def test_default_map_reduce(self):

		expected = {0:'Hello World'}

		result = shepherd.run(datasource = expected)

		self.assertEqual(expected, result)


	def test_array_input(self):
		data = ['Hello World']
		expected = {0:'Hello World'}

		result = shepherd.run(datasource = data)

		self.assertEqual(expected, result)


	def test_array_input_2(self):
		data = ['Hello', 'World']
		expected = {0:'Hello', 1:'World'}

		result = shepherd.run(datasource = data)

		self.assertEqual(expected, result)


	def test_example(self):

		expected = {'a': 2, 'on': 1, 'great': 1, 'Humpty': 3, 'again': 1, 'wall': 1, 'Dumpty': 2, 'men': 1, 'had': 1, 'all': 1, 'together': 1, "King's": 2, 'horses': 1, 'All': 1, "Couldn't": 1, 'fall': 1, 'and': 1, 'the': 2, 'put': 1, 'sat': 1}

		result = shepherd.run(
			datasource = example.datasource,
			mapfn = example.mapfn,
			reducefn = example.reducefn
		)

		self.assertEqual(expected, result)




if __name__ == '__main__':
	unittest.main()
