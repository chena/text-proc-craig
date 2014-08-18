import json
import sys
from processor import TextProcessor, Document
import numpy as np

def find_similar_pairs(data):
	"""
	Find the most similar document for each document in the collection, output the pairs
	"""
	processor = TextProcessor()

	for post in json.loads(data):
		# combine title and post content
		text = post['title'] + ' ' + post['description']
		doc = Document(post['link'], text, processor.process_doc(text.encode('utf-8')))
		processor.doc_collection.append(doc)

	similar_pairs = processor.similarity_analysis()
	data_output = {processor.doc_collection[f].link: processor.doc_collection[s].link for f, s in similar_pairs}
	
	with open('similar_0817.json', 'w') as file_output:
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
		find_similar_pairs(json_data)
		