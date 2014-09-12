# Craig Matcher

An app that allows you the find similar sublet postings in NYC on Craiglist based on the textual information contained in the documents. This project has various components and is still in progress.

* Text processing with [NLTK](http://www.nltk.org/), such as tokenization, stopwords removal and stemming.
* Building a VSM(vector space model) for a collection of documents using the [scikit-learn](http://scikit-learn.org/stable/index.html) library. Results are used to compare with my own implementation of the algorithms.
* Crawling data from NYC sublet postings on Craigslist using [Scrapy](http://doc.scrapy.org/en/latest/index.html). By default, each run will scrape the first 10 pages of [https://newyork.craigslist.org/sub/](https://newyork.craigslist.org/sub/), which contains 1000 postings with their titles and contents. The job is scheduled to run once a day.
* Data storage and retrieval using [MongoDB](http://www.mongodb.org/), with [Flask-PyMongo](http://flask-pymongo.readthedocs.org/en/latest/) and [scrapy-mongodb](http://sebdah.github.io/scrapy-mongodb/) (MongoDB pipeline for Scrapy).

## Brief Background - Text Processing and VSM

(Refer to linked pages for details)

In information retrieval, [tf-idf](http://en.wikipedia.org/wiki/Tf%E2%80%93idf) is a standard method for measuring the importance of a word in a document with resepct to a corpus. 

A [vector space model](http://en.wikipedia.org/wiki/Vector_space_model) is a way to represent a collection of documents in a high-dimensional space, with each row of the matrix being a document represented by a sparse vector composed of td-idf weights.

With the vector representations, we can mesaure the similarity between two documents using [consine similarity](http://en.wikipedia.org/wiki/Cosine_similarity).

## Setup

There are a couple tools we need to install to run the application. Assuming that you alreayd have `pip` installed, you can either run `pip install -r requirements.txt` or install these packages individually:

```
pip install nltk
pip install -U numpy scipy scikit-learn
pip install Scrapy
pip install beautifulsoup4
pip install Flask-PyMongo
pip install scrapy-mongodb
```
## Usage

To run the app:

* Run `python craig.py` to start the server
* Visit the running app at `http://localhost:7000/`

## Demo
<img src="https://raw.githubusercontent.com/chena/text-proc-craig/master/craig.png">

