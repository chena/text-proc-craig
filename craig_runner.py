import json
import sys
from processor import TextProcessor
import numpy as np

# TODO: do we need this wrapper class to represent document?
class CraigDocument:
	def __init__(self, id):
		self.id = id
	
	def set_text(self, text):
		self.text = text

def save_similar_pairs(json_data):
	"""
	Find the most similar document for each document in the collection, output the pairs
	"""
	processor = TextProcessor()
	processed_collection = []
	original = []
	data = json.loads(json_data)

	for post in data:
		# combine title and post content
		doc = post['title'] + ' ' + post['description']
		original.append(doc) # TODO: create a CraigDocument instance here instead
		processed_collection.append(processor.process_doc(doc))


	# similarity analysis
	sim_mat = processor.compute_similarity_sklearn(processed_collection)
	# zero out diagonal that are all one's - doc compares to themselves should be exact match
	# TODO: maybe move this to utility
	np.fill_diagonal(sim_mat, 0)

	# get the max value of each row
	most_similar_scores = sim_mat.max(1)
	most_similar_indices = sim_mat.argmax(1)
	similar_pairs = zip(range(processor.doc_count), most_similar_indices)

	data_output = {data[f]['link']: data[s]['link'] for f, s in similar_pairs}

	with open('similar_0813.json', 'w') as file_output:
		json.dump(data_output, file_output)

	# print original text of similar pairs
	"""
	for f, s in similar_pairs:
		print original[f].encode('utf-8')
		print original[s].encode('utf-8')
		print
	"""

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >> sys.stderr, 'usage: %s json_file' % sys.argv[0]
	else:
		json_data = open(sys.argv[1]).read()
		save_similar_pairs(json_data)
		