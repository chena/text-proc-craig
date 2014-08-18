from flask import Flask, render_template, request
from processor import TextProcessor, Document
import json
import re
from bs4 import BeautifulSoup
import urllib3
import numpy as np

app = Flask(__name__)

# initial setup
# TODO: should load the most recent json (or read from DB)
# http://flask-pymongo.readthedocs.org/en/latest/
# How to refresh data for a running app?
processor = TextProcessor()
known_pairs = json.load(open('similar_0813.json'))

json_data = open('craig_0817.json').read()
for post in json.loads(json_data):
	# combine title and post content
	text = post['title'] + ' ' + post['description']
	doc = Document(post['link'], text, processor.process_doc(text.encode('utf-8')))
	processor.doc_collection.append(doc)
processor.build_doc_matrix()

@app.route("/", methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		return render_template('index.html')

	url = request.form['url']
	domain = 'newyork.craigslist.org/'
	print url
	# naive checking
	if not domain in url:
		# should give some kind of error
		return render_template('index.html')

	#if known_pairs.has_key(url):
	#	return render_template('index.html', qry=url, link=known_pairs[url])

	# unseen document
	qry_doc = _get_qry_page(url)
	processed = processor.process_doc(qry_doc.encode('utf-8'))
	vect = processor.vectorizer.transform([' '.join(processed)]) # this returns a sparse vector of csr_matrix type
	sim_vect = processor.doc_mat * vect.T
	
	top_ind = processor.get_top_ind(sim_vect.A.flatten(), 10)
	matches = [processor.doc_collection[i] for i in top_ind]
	for m in matches:
		print m.link

	max_ind = np.argmax(sim_vect.A)
	match_doc = processor.doc_collection[max_ind]
	
	#top_terms = processor.get_top_terms(processor.doc_mat[max_ind,:], 10)
	#print top_terms

	return render_template('index.html', qry=url, qry_desc=qry_doc, link=match_doc.link, desc=match_doc.original)

def _get_qry_page(url):
	http = urllib3.PoolManager()
	page = http.request('GET', url).data
	data = BeautifulSoup(page)
	return data.h2.text.strip() + ' ' + data.find(id='postingbody').text.strip() 

if __name__ == "__main__":
    app.run(debug=True, port=7000)

