import requests
from bs4 import BeautifulSoup
import re
import json
from book import Book
from review import Review
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

analyzer = SentimentIntensityAnalyzer()
"""Module that retrieves information about books. This information contains:
	- link
	- brand
	- reviews
	- isbn
"""


class Retriever:

	@staticmethod
	def get_books_links(base_url, category):
		"""Given a base url and a category of books, return a list of links
		each representing a book."""
		books_info = []

		page = requests.get(base_url + category)
		soup = BeautifulSoup(page.content, 'html.parser')
		d = soup.find_all("div", {"class": "js-tooltipTrigger tooltipTrigger"})

		for entry in d:
			entry = soup.find_all("a", {"class": "pollAnswer__bookLink"}, href=True)
			for info in entry:
				book_link = info['href']
				# Puts links into a list
				books_info.append(base_url + book_link)
		return(books_info)


	@staticmethod
	def get_book_brand(book_link):
		"""Given a url representing a book, return the brand of that book"""
		book_brand = []
		page = requests.get(book_link)
		soup = BeautifulSoup(page.content, 'html.parser')

		brand = soup.find_all("h1", {"class": "gr-h1 gr-h1--serif"})[0]
		book_brand.append(brand)
		return  brand.get_text().strip()


	@staticmethod
	def get_book_isbn(book_link):
		page_ISBN = requests.get(book_link)
		soup_ISBN = BeautifulSoup(page_ISBN.content, 'html.parser')
		isbn = soup_ISBN.find("span", {"itemprop": "isbn"})
		return int(isbn.get_text().strip())


	@staticmethod
	def get_book_reviews(book_link):
		"""Given a url representing a book, return the reviews for that book.
		The reviews are stored in a dictionary. Each review has an id as the key,
		and a dictionary as the value. The value stores the date and the contents
		of the review, as strings.
		"""
		page = requests.get(book_link)
		soup = BeautifulSoup(page.content, 'html.parser')

		reviews = {}

		dates = soup.find_all("a", {"class": "reviewDate createdAt right"}, href=True)
		contents = soup.find_all("div", {"class": "reviewText stacked"})

		analyser = SentimentIntensityAnalyzer()

		for id in range(len(contents)):

			score = analyser.polarity_scores(contents[id].get_text().strip())
			key = str(id)
			review = Review(date=dates[id].get_text().strip(), content=contents[id].get_text().strip(),score = score)
			reviews[key] = review.create_dictionary()
			print(contents[id].get_text().strip())


		return reviews

	@staticmethod
	def dump_reviews_to_file(filename, books):
		"""Creates a .json file using information about books.
		The file will be structured as a list of dictionaries.
		Each of these dictionaries will contain the following:
			- link - string
			- brand - string
			- reviews - dictionary

		params:
		books -- A list of Book objects
		filename -- The name of the json file where the results are written
		"""
		with open(filename, 'w', encoding='utf-8') as f:
			book_dicts = []
			for book in books:
				book_dicts.append(book.create_dictionary())

			json.dump(book_dicts, f, ensure_ascii=False, indent=4)

		print("Finished writing info to file", filename)


	@staticmethod
	def retrieve_books(base_url, category, num_books):
		# List of links to books

		books_links = Retriever.get_books_links(base_url, category)



		# List of books containing items of type 'Book'
		books = []

		# Get brand and reviews for each book
		i = 0
		for book_link in books_links:
			if i == num_books:
				break

			book_brand = Retriever.get_book_brand(book_link)
			book_isbn = Retriever.get_book_isbn(book_link)
			book_reviews = Retriever.get_book_reviews(book_link)
			books.append(Book(link=book_link, brand=book_brand,isbn=book_isbn, reviews=book_reviews))
			i += 1
		return books
