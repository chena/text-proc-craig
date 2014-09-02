from flask import Flask, render_template, request
from processor import TextProcessor, Document
import re
from bs4 import BeautifulSoup
import urllib3
import numpy as np
from flask.ext.pymongo import PyMongo
import os
import sys

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGOHQ_URL')
mongo = PyMongo(app)
processor = TextProcessor()

with app.app_context():
	processor.map_data(mongo.db.postings.find())
	processor.build_doc_matrix()

@app.route('/', methods=['GET', 'POST'])
def main():
	if request.method == 'GET':
		return render_template('index.html')

	url = request.form['url'].strip()
	domain = 'newyork.craigslist.org/'

	if not domain in url:
		return render_template('index.html', error='Please enter a valid URL')

	# process unseen document
	try:
		qry_doc = _get_qry_doc(url)
	except CraigParseError, e:
		return render_template('index.html', error=e.msg)
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

	title, desc = data.h2, data.find(id='postingbody')
	expired_msg = 'This posting has been deleted by its author'
	not_found_msg = 'No web page for this address'

	if title:
		title = title.text.strip()
		if expired_msg in title:
			raise CraigParseError(expired_msg)
	if desc:
		desc = desc.text.strip()
		if not_found_msg in desc:
			raise CraigParseError(not_found_msg)
	if not title or not desc:
		raise CraigParseError('The content of the queried page cannot be processed')

	return Document(url, title, desc, 
			processor.process_doc((title + ' ' + desc).encode('utf-8')))

class CraigParseError(Exception):
	def __init__(self, msg):
		self.msg = msg
	
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 7000))
	app.run(host='0.0.0.0', port=port, debug=True)

