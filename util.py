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

class Document(object):
	def __init__(self, id, text):
		self.id = id
		self.text = text

class TextProcessor(object):
	def __init__(self):
		self.stop_words = stopwords.words('english')
		self.porter = PorterStemmer()
		self.doc_count = 0
		self.inverse_list = defaultdict(int) # inverse list of words to number of documents

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

	def gen_matrix(self, text):
		word_counts = [dict(Counter(tokens)) for tokens in text]
		word_list = self.inverse_list.keys()

		# prepare the document matrix
		mat = np.zeros((self.doc_count, len(self.inverse_list)))

		index = 0
		idf_weights = self._gen_idf_weights(word_list)
		print idf_weights

		for wc in word_counts:
			for w, c in wc.items():
				mat[index, word_list.index(w)] = c
			index += 1

		# apply the idf-weigts to each column of the matrix corresponding to each term
		for i in range(mat.shape[1]):
			mat[:, i] *= idf_weights[i]

		print mat
		return mat

	def _gen_idf_weights(self, wlist):
		return map(lambda w: math.log(self.doc_count / (self.inverse_list[w]), 2), wlist)

	def consine_similarity(self, d1, d2):
		# the denominator is equivalent to (math.sqrt(np.dot(d1, d1)) * math.sqrt(np.dot(d2, d2)))
		# linnalg.norm calculates L2 norm by default
		return np.dot(d1, d2) / (np.linalg.norm(d1) * np.linalg.norm(d2))

	def compute_similarity_sklearn(self, text):
		vectorizer = TfidfVectorizer()
		collection = [' '.join(doc) for doc in processed_collection]
		mat = vectorizer.fit_transform(collection)
		# sim = cosine_similarity(mat[0:1], mat)
		# generate the similarity matrix
		print (mat * mat.T).A

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
		documents = [
			"The sky is blue",
			"The sun is bright",
			"The sun in the sky is bright",
			"We can see the shining sun, the bright sun"]

		for doc in documents:
			processed_collection.append(processor.process_doc(doc))

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

		"""
		TODO: write some tests for this class
		"""


