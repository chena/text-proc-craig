from flask import Flask, render_template, request
from processor import TextProcessor, Document
import json
import re
from bs4 import BeautifulSoup
import urllib3
import numpy as np
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)
processor = TextProcessor()
with app.app_context():
	processor.map_data(mongo.db.postings.find())
	processor.build_doc_matrix()
# How to refresh data for a running app?
#known_pairs = json.load(open('similar_0813.json'))
#json_data = open('craig_0817.json').read()

@app.route("/", methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		return render_template('index.html')

	url = request.form['url'].strip()
	domain = 'newyork.craigslist.org/'

	if not domain in url:
		# TODO: should give some kind of error
		return render_template('index.html')

	#if known_pairs.has_key(url):
	#	return render_template('index.html', qry=url, link=known_pairs[url])

	# process unseen document
	qry_doc = _get_qry_doc(url)
	vect = processor.vectorizer.transform([' '.join(qry_doc.processed)]) # this returns a sparse vector of csr_matrix type

	# build similarity matrix and extract top matches
	sim_vect = processor.doc_mat * vect.T
	# we need to first convert the sparse array to dense form and flatten it
	top_sim_ind = processor.get_top_ind(sim_vect.A.flatten(), 10)
	matches = [processor.doc_collection[i] for i in top_sim_ind]

	# exclude exact match
	if matches[0].link == qry_doc.link:
		del matches[0]

	return render_template('index.html', qry=qry_doc, matches=matches)

def _get_qry_doc(url):
	http = urllib3.PoolManager()
	page = http.request('GET', url).data
	data = BeautifulSoup(page)
	title, desc = data.h2.text.strip(), data.find(id='postingbody').text.strip() 
	text = title + ' ' + desc
	return Document(url, title, desc, processor.process_doc(text.encode('utf-8')))

if __name__ == '__main__':
    app.run(debug=True, port=7000)

