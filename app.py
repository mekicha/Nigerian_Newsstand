from flask import Flask, request, render_template, jsonify, url_for
from goose import Goose 
import requests
import bs4


app = Flask(__name__)
g = Goose()
index_links = {}

@app.route('/')
@app.route('/index')
def index():
	return index_links
	return render_template('index.html')


@app.route('/premium')
def premium():
	""" Get top news from premiumtimesng.com """
	url = "http://premiumtimesng.com/category/news/headlines"
	soup = make_soup(url)
	urls = []
	links = []
	titles = []
	articles =[]
	images = []
	pos = 0
	for link in soup.select('.a-story a'):
		urls.append(link)
	for url in urls:
		pos = str(url).find('.html')
		if pos == -1:
			urls.remove(url)
		else:
			links.append(str(url)[9:pos+5])
	links = make_unique(links)
	index_links['premium'] = [links]
	for url in links:
		article = g.extract(url=url)
		titles.append(article.title)
		images.append(article.top_image.src)
		articles.append(article.cleaned_text[:150])

	return render_template('premium.html', params =zip(links,titles, images,articles)
		                  )


@app.route('/sahara')
def sahara():
	"""Get top news items from saharareporters.com """
	url = 'http://saharareporters.com/news'
	soup = make_soup(url)
	urls =     []
	links =    []
	titles =   []
	articles = []
	images =   []
	return soup

@app.route('/sunnews')
def sunnews():
	"""Get top news items from sunnewsonline.com """
	pos = 0
	last = 0
	links = []
	titles = []
	articles = []
	url = 'http://www.sunnewsonline.com/new/category/cover'
	soup = make_soup(url)
	for link in soup.select('.image-link'):
		pos = str(link).find('http')
		last = str(link).find('title', pos)
		links.append(str(link)[pos:last-2])
	links = make_unique(links)
	for url in links:
		article = g.extract(url=url)
		titles.append(article.title)
		articles.append(article.cleaned_text[:150])
	return render_template('sunnews.html', params = zip(links, titles, articles))
	


@app.route('/punch')
def punch():
	url = 'http://www.punchng.com/news'


@app.route('/thenation')
def thenation():
	"""Get top news items from thenationonlineng"""
	pos = 0
	links = []
	titles = []
	articles = []
	url = 'http://thenationonlineng.net/category/news/'
	soup = make_soup(url)
	for link in soup.select('.post-img a'):
		pos = str(link).find('>')
		links.append(str(link)[9:pos-1])
	links = make_unique(links)
	for url in links:
		article = g.extract(url=url)
		titles.append(article.title)
		articles.append(article.cleaned_text[:150])
	return render_template('thenation.html', params = zip(links, titles, articles))




def get_url(url):
	"""Get webpage of given url and returns url body as r.text"""
	headers = {'user-agent':'Mozilla/42.0'}
	r = requests.get(url, headers=headers)
	return r.text

def make_soup(url):
	"""Takes a url and parses its the returned body using BeautifulSoup"""
	text = get_url(url)
	soup = bs4.BeautifulSoup(text,'lxml')
	return soup

def make_unique(original_list):
	"""Takes an original list and returns a unique list without duplicate elements"""
	unique_list = []
	[unique_list.append(obj) for obj in original_list if obj not in unique_list]
	return unique_list




if __name__ == "__main__" :
	app.run(debug = True)
	