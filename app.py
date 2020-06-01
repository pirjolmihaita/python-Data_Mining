# examples/things.py
# Let's get this party started!
from wsgiref.simple_server import make_server
import falcon
import json
from json import dumps, loads
from mongoengine import *
from data_operations import Operations
from data_operations import database_name
from analyser import Analyser
from retriever import Retriever

# Falcon follows the REST architectural style, meaning (among
# other things) that you think in terms of resources and state
# transitions, which map to HTTP verbs.
class AnalyseResource:
    def on_get(self, req, resp):
        connect(database_name)
        if Operations.getBooksCount() == 0:
            resp.body = dumps("No books in database. You should retrieve them first :(")
            resp.status = falcon.HTTP_200
        else:
            books = Operations.getBooks()
            books_scores = Analyser.analyse_books(books)

            resp.body = dumps(books_scores)
            resp.status = falcon.HTTP_200

class AnalyseOneBook:
    def on_get(self, req, resp, isbn):
        connect(database_name)
        book  = Operations.getBookByISBN(isbn)
        book = book.to_json()
        book = loads(book)
        resp.body = dumps(book)
        resp.status = falcon.HTTP_200

class RetrieveResource:
    def on_get(self, req, resp):

        validate_params = True
        resp.status = falcon.HTTP_200
        if 'base_url' not in req.params:
            validate_params = False
        if 'category' not in req.params:
            validate_params = False

        num_books = 3

        if (validate_params is True):

            connect(database_name)
            books = Retriever.retrieve_books(req.params['base_url'], req.params['category'], num_books)
            Operations.insertBooks(books)

            resp.body = dumps("Inserted books in database")
            resp.status = falcon.HTTP_200

class DeleteResource:
    def on_get(self, req, resp):
        connect(database_name)
        Operations.deleteAllBooks()

        resp.body = dumps("Deleted books in database")
        resp.status = falcon.HTTP_200

# falcon.API instances are callable WSGI apps
# in larger applications the app is created in a separate file
app = falcon.API()

# Resources are represented by long-lived class instances
analyse_things = AnalyseResource()
retrieve_things = RetrieveResource()
delete_things = DeleteResource()
analyse_one_book = AnalyseOneBook()

# things will handle all requests to the '/things' URL path
app.add_route('/analyse_books',analyse_things)
app.add_route('/analyse_one_book/{isbn}', analyse_one_book)
app.add_route('/params',retrieve_things)
app.add_route('/delete_books',delete_things)


if __name__ == '__main__':
    with make_server('', 8000, app) as httpd:
        print('Serving on port 8000...')

        # Serve until process is killed
        httpd.serve_forever()
