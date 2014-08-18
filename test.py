from __future__ import division
import unittest
from processor import TextProcessor
import numpy as np
import math

class ProcessorTest(unittest.TestCase):

	@classmethod
	def setUpClass(self):
		self.documents = (
			'The sky is very blue',
			'The sun is bright',
			'The sun in the sky is bright',
			'We can see the shining sun, the bright SUN')

	def setUp(self):
		self.processor = TextProcessor()
	
	def test_process_doc(self): 
		self.assertEqual(self.processor.process_doc(self.documents[0]), ['sky', 'blue'])
		self.assertEqual(self.processor.process_doc(self.documents[3]), ['see', 'shine', 'sun', 'bright', 'sun'])
		self.assertEqual(self.processor.doc_count, 2)

	def test_gen_matrix(self):
		for doc in self.documents:
			self.processor.doc_collection.append(self.processor.process_doc(doc))
		mat = self.processor.gen_matrix()
		print mat
		# verify the generated inverse list
		self.assertEqual(self.processor.inverse_list, {'blue': 1, 'shine': 1, 'sun': 3, 'sky': 2, 'see': 1, 'bright': 3})

		# verify the tf-idf calculation
		expected = [[math.log(4), 0, 0, math.log(2), 0, 0], 
 					[0, 0, math.log(4 / 3), 0, 0, math.log(4 / 3)], 
					[0, 0, math.log(4 / 3), math.log(2), 0, math.log(4 / 3)], 
					[0, math.log(4), 2 * math.log(4 / 3), 0, math.log(4), math.log(4 / 3)]]
		np.testing.assert_array_equal(self.processor.doc_mat, expected)

	def test_consine_similarity(self):
		# the formula is the dot product of d1 and d2 over the product of their euclidean lengths
		d1, d2 = [[1, 0, 2, 4], [0, 3, 2, 1]]
		self.assertEqual(self.processor.consine_similarity(d1, d2), 8 / (math.sqrt(21) * math.sqrt(14)))

	def test_get_top_items(self):
		arr = np.array([2, 6, 8, 4, 5, 3])
		np.testing.assert_array_equal(self.processor.get_top_ind(arr, 3), [2, 1, 4])

if __name__ == '__main__':
	unittest.main()

