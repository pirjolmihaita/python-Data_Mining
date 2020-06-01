from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from book import Book


"""Module that analyses information about books based on their reviews,
"""


class Analyser:

	@staticmethod
	def algorithm(scores):
		"""Simple algorithm that computes the percent of positive and negative
		reviews for a book based on scores returned by the sentiment
		analysis

		returns: two values, positive percent and negative percent
		"""
		pos_reviews = 0
		neg_reviews = 0
		total_reviews = len(scores)

		for score in scores:
			if (score['pos'] > score['neg']):
				pos_reviews += 1
			else:
				neg_reviews += 1

		return pos_reviews / total_reviews * 100, neg_reviews / total_reviews * 100


	@staticmethod
	def perform_sentiment_analysis(book):
		"""Compute statistics about reviews for a book"""
		scores = []
		analyzer = SentimentIntensityAnalyzer()

		for review in book['reviews'].values():
			score = analyzer.polarity_scores(review['content'])
			scores.append(score)

		(pos_percent, neg_percent) = Analyser.algorithm(scores)
		print("Book analysed:", book['brand'])
		print("\tpositive reviews:", pos_percent, "%")
		print("\tnegative reviews:", neg_percent, "%\n")
		return book['brand'],book['isbn'], pos_percent, neg_percent


	@staticmethod
	def load_reviews_from_file(filename, books):
		"""Load information about the books from a json file"""
		with open('demo.json','r',encoding= 'utf-8') as f:
			data = json.load(f)
			for item in data:
				books.append(Book(link=item['link'], brand=item['brand'], reviews=item['reviews'],isbn=item['isbn']))


	@staticmethod
	def analyse_books(books):
		books_scores = dict()
		for book in books:
			brand,isbn, pos, neg = Analyser.perform_sentiment_analysis(book)
			books_scores[brand] = {"isbn":isbn,"positive": pos, "negative": neg}
		return books_scores



