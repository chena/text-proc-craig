from flask import Flask, render_template, request
#from util import TextProcessor
import json

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def post_url():
	if request.method == 'POST':
		# get URL
		url = request.form['url']
		print url
		known_pairs = json.loads(open('similar_links.json').read())
		similar_link = known_pairs[url] if known_pairs.has_key(url) else None
		return render_template('index.html', link=similar_link)

	return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=7000)