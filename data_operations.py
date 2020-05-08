from mongoengine import *
from book import Book

database_name = 'books_database'

class BookEntry(Document):
    link = StringField(required=True, max_length=200)
    brand = StringField(required=True, max_length=200)
    isbn = IntField(required=True)
    reviews = DictField(required=True)

class Operations:
    """Class that defines operations performed on books database.
    """

    @staticmethod
    def insertBook(book):
        """Insert a book in the database if a book containing the same isbn code
        doesn't exist already"""
        if not BookEntry.objects(isbn=book.isbn):
            book_entry = BookEntry(link=book.link, brand=book.brand, isbn=book.isbn, reviews=book.reviews)
            book_entry.save()
            print("[INSERT] Inserted book {} in the database".format(book.brand))
        else:
            print("[INSERT] Error: Book {} was already in the database".format(book.brand))


    @staticmethod
    def insertBooks(books):
        for book in books:
            Operations.insertBook(book)


    @staticmethod
    def getBookByISBN(isbn):
        return BookEntry.objects(isbn=isbn)

    @staticmethod
    def getBooks():
        return BookEntry.objects()

    @staticmethod
    def getBooksCount():
        return BookEntry.objects.count()

    @staticmethod
    def deleteBookByISBN(isbn): #cum de isbn este isbn
        BookEntry.objects(isbn=isbn).delete()
        print("[DELETE] Deleted book with isbn {} from database".format(isbn))

    @staticmethod
    def deleteAllBooks():
        BookEntry.objects.delete()
        print("[DELETE] Deleted all books from database")
