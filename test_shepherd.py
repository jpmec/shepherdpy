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




	def test_word_counting_1(self):
		data = ['one fish two fish red fish blue fish']

		expected = {'one':1, 'two':1, 'red':1, 'blue':1, 'fish':4}

		result = shepherd.run(
			datasource = data,
			mapfn = shepherd.map_word_count,
			reducefn = shepherd.reduce_word_count,
		)

		self.assertEqual(expected, result)




	def test_word_counting_2(self):
		data = ['one fish', 'two fish', 'red fish', 'blue fish']

		expected = {'one':1, 'two':1, 'red':1, 'blue':1, 'fish':4}

		result = shepherd.run(
			datasource = data,
			mapfn = shepherd.map_word_count,
			reducefn = shepherd.reduce_word_count,
		)

		self.assertEqual(expected, result)




	def test_CustomServer(self):
		data = ['one fish', 'two fish', 'red fish', 'blue fish']
		expected = {0: 'one fish', 1: 'two fish', 2: 'red fish', 3: 'blue fish'}

		result = shepherd.run(
			datasource = data,
			server = shepherd.Server,
		)

		self.assertEqual(expected, result)




	def test_WordCountServer(self):
		data = ['one fish', 'two fish', 'red fish', 'blue fish']

		expected = {'one':1, 'two':1, 'red':1, 'blue':1, 'fish':4}

		result = shepherd.run(
			datasource = data,
			server = shepherd.WordCountServer,
		)

		self.assertEqual(expected, result)




if __name__ == '__main__':
	unittest.main()
