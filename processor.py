from __future__ import division
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk import PorterStemmer
from collections import Counter
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import sys
import string
import math
import numpy as np
import os

class Document:
	def __init__(self, link, original, processed):
		self.link = link
		self.original = original
		self.processed = processed
		self.rank_list = []

class TextProcessor(object):
	def __init__(self):
		self.stop_words = stopwords.words('english')
		self.porter = PorterStemmer()
		self.vectorizer = TfidfVectorizer()

		self.doc_count = 0
		self.inverse_list = defaultdict(int) # inverse list of words to number of documents
		self.doc_collection = []
		self.word_list = []
		self.doc_mat = None # document matrix

	def process_doc(self, doc):
		self.doc_count += 1
		processed = []

		text = doc.translate(None, string.punctuation)
		words = word_tokenize(text)

		for w in words:
			w = w.lower()
			if w not in self.stop_words:
				stemmed = self.porter.stem(w)
				processed.append(stemmed)

		for w in set(processed):
			self.inverse_list[w] += 1

		return processed

	def gen_matrix(self):
		self.word_list = self.inverse_list.keys()
		word_counts = [dict(Counter(tokens)) for tokens in self.doc_collection]
		idf_weights = self._gen_idf_weights(self.word_list)

		# prepare the document matrix
		mat = np.zeros((self.doc_count, len(self.inverse_list)))

		index = 0
		for wc in word_counts:
			for w, c in wc.items():
				mat[index, self.word_list.index(w)] = c
			index += 1

		# apply the idf-weigts to each column of the matrix corresponding to each term
		for i in range(mat.shape[1]):
			mat[:, i] *= idf_weights[i]

		self.doc_mat = mat

	def _gen_idf_weights(self, wlist):
		# we could add-1 smoothing to avoid division by zero
		return map(lambda w: math.log(self.doc_count / self.inverse_list[w]), wlist)

	def consine_similarity(self, d1, d2):
		# the denominator is equivalent to (math.sqrt(np.dot(d1, d1)) * math.sqrt(np.dot(d2, d2)))
		# linnalg.norm calculates L2 norm by default
		return np.dot(d1, d2) / (np.linalg.norm(d1) * np.linalg.norm(d2))

	"""
	using scikit-learn library #
		step 1: build the document matrix with tf-idf weights for the collection
		step 2: compute similarity between each document against all other documents, resulting in an n x n matrix
		step 3: extract the most similar documents TODO: extract a ranked list
	"""

	def build_doc_matrix(self):
		# transoforms the corpus into tf-idf representation
		# returning a sparse matrix
		text = [' '.join(doc.processed) for doc in self.doc_collection]
		self.doc_mat = self.vectorizer.fit_transform(text)
		self.word_list = self.vectorizer.get_feature_names()
		
	def compute_similarity_sklearn(self):
		self.build_doc_matrix()

		# .T gets you the transpose matrix and .A converts from sparse to normal dense representation
		# note: no need to normalize, since Vectorizer will return normalized tf-idf
		mat = self.doc_mat
		return (mat * mat.T).A

	def similarity_analysis(self):
		sim_mat = self.compute_similarity_sklearn()

		# zero out diagonal that are all one's - doc compares to themselves should be exact match
		# TODO: maybe move this to utility
		np.fill_diagonal(sim_mat, 0)

		# get the max value of each row
		most_similar_indices = sim_mat.argmax(1)

		# return pairs of similar documents
		return zip(range(self.doc_count), most_similar_indices)

	def get_top_ind(self, vect, num=10):
		"""
		find the indices of the top n items in the given vector
		"""
		print vect.shape
		top = np.argpartition(vect, -num)[-num:]
		return top[np.argsort(vect[top])][::-1]

	#def get_rank_list(self, vect, num=10):

		
		"""
		dense_mat = mat.A
		sorted_indices = np.argsort(dense_mat)
		#for in in range(dense_mat.shape[0]):
		for i in range(5): # just look at first 5 docs for now
			rank = dense_mat[i, :][sorted_indices[i, :]]
			print rank
		"""

		"""
		for i in range(dense_mat.shape[0]):
			vect = dense_mat[i,:]
			top10 = self.get_top_terms(vect, 10)
			for ind in top10:
				print self.word_list[ind]
			print
		"""

# using some small datasets for testing purposes
if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >> sys.stderr, 'usage: %s data_folder' % sys.argv[0]
	else:
		processor = TextProcessor()
		processed_collection = []
		dir_name = sys.argv[1]

		# traverse the data directory and process each document
		for fname in os.listdir(dir_name):
			doc = open(os.path.join(dir_name, fname)).read()
			processed_collection.append(processor.process_doc(doc))

		"""
		# generate the document matrix
		mat = processor.gen_matrix(processed_collection)

		d1, d2, d3, d4 = mat
		
		print mat.shape

		print 'd1 & d2 %s' % processor.consine_similarity(d1, d2)
		print 'd1 & d3 %s' % processor.consine_similarity(d1, d3)
		print 'd1 & d4 %s' % processor.consine_similarity(d1, d4)
		print 'd2 & d3 %s' % processor.consine_similarity(d2, d3)
		print 'd2 & d4 %s' % processor.consine_similarity(d2, d4)
		print 'd3 & d4 %s' % processor.consine_similarity(d3, d4)
		"""

		processor.compute_similarity_sklearn(processed_collection)

		"""
		# generate the document matrix
		mat = processor.gen_matrix(processed_collection)
		print processor.inverse_list
		d1, d2, d3, d4 = mat

		print 'd1 & d1 %s' % processor.consine_similarity(d1, d1)
		print 'd1 & d2 %s' % processor.consine_similarity(d1, d2)
		print 'd1 & d3 %s' % processor.consine_similarity(d1, d3)
		print 'd1 & d4 %s' % processor.consine_similarity(d1, d4)
		print 'd2 & d3 %s' % processor.consine_similarity(d2, d3)
		print 'd2 & d4 %s' % processor.consine_similarity(d2, d4)
		print 'd3 & d4 %s' % processor.consine_similarity(d3, d4)
		"""


