from flask import Flask, request, render_template, jsonify, url_for
from goose import Goose 
import requests
import bs4


app = Flask(__name__)
g = Goose()

@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')


@app.route('/premium')
def premium():
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
	for url in links:
		article = g.extract(url=url)
		titles.append(article.title)
		images.append(article.top_image.src)
		articles.append(article.cleaned_text[:150])

	return render_template('premium.html', params =zip(links,titles, images,articles)
		                  )


@app.route('/sahara')
def sahara():
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

@app.route('/thisday')
def thisday():
	url = ' http://www.thisdaylive.com/articles/'



def get_url(url):
	headers = {'user-agent':'Mozilla/42.0'}
	r = requests.get(url, headers=headers)
	return r.text

def make_soup(url):
	text = get_url(url)
	soup = bs4.BeautifulSoup(text)
	return soup

def make_unique(original_list):
	unique_list = []
	[unique_list.append(obj) for obj in original_list if obj not in unique_list]
	return unique_list




if __name__ == "__main__" :
	app.run(debug = True)
	