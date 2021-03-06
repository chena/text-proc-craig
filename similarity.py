import json
import sys
from processor import TextProcessor, Document
import numpy as np

def find_similar_pairs(data):
	"""
	Find the most similar document for each document in the collection, output the pairs
	"""
	processor = TextProcessor()
	processor.map_json_data(data)
	similar_pairs = processor.similarity_analysis()
	data_output = {processor.doc_collection[f].link: processor.doc_collection[s].link for f, s in similar_pairs}
	
	with open('similar_0817.json', 'w') as file_output:
		json.dump(data_output, file_output)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print >> sys.stderr, 'usage: %s json_file' % sys.argv[0]
	else:
		json_data = open(sys.argv[1]).read()
		find_similar_pairs(json_data)
		