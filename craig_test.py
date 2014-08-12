import json
import sys
from util import TextProcessor

class CraigDocument(object):
	def __init__(self, id):
		self.id = id
	
	def set_text(self, text):
		self.text = text

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >> sys.stderr, 'usage: %s json_file' % sys.argv[0]
	else:
		processor = TextProcessor()
		processed_collection = []

		data = open(sys.argv[1]).read()
		for post in json.loads(data):
			doc = post['title'] + ' ' + post['title']
			print doc
			processed_collection.append(processor.process_doc(doc))

		"""
		sim_mat = processor.compute_similarity_sklearn(processed_collection[:10])
		
		print sim_mat.shape
		for i in range(sim_mat.shape[0]):
			print processed_collection[i]
			best = max(sim_mat[i,:])
			print best
		"""

		# generate the document matrix
		mat = processor.gen_matrix(processed_collection)

		d1, d2, d3, d4, d5, d6, d7, d8, d9, d10 = mat[:10]
		
		print mat.shape

		print 'd1 & d2 %s' % processor.consine_similarity(d1, d2)
		print 'd1 & d3 %s' % processor.consine_similarity(d1, d3)
		print 'd1 & d4 %s' % processor.consine_similarity(d1, d4)
		print 'd1 & d5 %s' % processor.consine_similarity(d1, d5)
		print 'd1 & d6 %s' % processor.consine_similarity(d1, d6)
		print 'd1 & d7 %s' % processor.consine_similarity(d1, d7)
		print 'd1 & d8 %s' % processor.consine_similarity(d1, d8)
		print 'd1 & d9 %s' % processor.consine_similarity(d1, d9)
		print 'd1 & d10 %s' % processor.consine_similarity(d1, d10)


		print 'd2 & d3 %s' % processor.consine_similarity(d2, d3)
		print 'd2 & d4 %s' % processor.consine_similarity(d2, d4)
		print 'd3 & d4 %s' % processor.consine_similarity(d3, d4)
		