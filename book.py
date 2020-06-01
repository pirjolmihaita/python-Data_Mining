class Book:
    def __init__(self, link, brand, reviews,isbn):
        self.link = link
        self.brand = brand
        self.isbn = isbn
        self.reviews = reviews



    def create_dictionary(self):
        return {
            'link': self.link,
            'brand': self.brand,
            'isbn': self.isbn,
            'reviews': self.reviews,
        }
