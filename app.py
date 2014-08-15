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
# How to refresh data for a running app?
processor = TextProcessor()
known_pairs = json.load(open('similar_0813.json'))

json_data = open('craig_0813.json').read()
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

	if known_pairs.has_key(url):
		return render_template('index.html', qry=url, link=known_pairs[url])

	# unseen document
	qry_doc = _get_qry_page(url)
	processed = processor.process_doc(qry_doc.encode('utf-8'))
	vect = processor.vectorizer.transform([' '.join(processed)])
	sim_vect = processor.doc_mat * vect.T

	max_ind = np.argmax(sim_vect.A)
	match_doc = processor.doc_collection[max_ind]

	return render_template('index.html', qry=url, link=match_doc.link, desc=match_doc.original)

	# TODO: process the text and analyze


"""
@app.route("/", methods=['GET', 'POST'])
def main():
	if request.method == 'POST':
		# get URL
		url = request.form['url']
		similar_link = known_pairs[url] if known_pairs.has_key(url) else None
		return render_template('index.html', link=similar_link)

	return render_template('index.html')
"""

# move this to util
def _get_qry_page(url):
	http = urllib3.PoolManager()
	page = http.request('GET', url).data
	data = BeautifulSoup(page)
	return data.h2.text.strip() + ' ' + data.find(id='postingbody').text.strip() 


if __name__ == "__main__":
    app.run(debug=True, port=7000)

