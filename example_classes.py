# data = {x, y, string}

# record_book = {
# author = ""
# published_year = int
# number of times borrowed = int
# ISBN-13 = string
# }

# list_of_records = [book1, book2, book3, etc]

# list_of_records[0]["ISBN-13"]

class Book():

    def __init__(self, title, author):
        """Initialises the class"""
        self.title = title
        self.author = author
        self.tags = []
        self.published_year = 0
        self.n_borrowed = 0
        self.last_borrowed = ""
        self.ISBN_13 = ""
        self.is_borrowed = False

    
        
    def borrow_a_book(self, name):
        self.n_borrowed += 1
        self.last_borrowed = name
        self.is_borrowed = True

    def return_a_book(self):
        self.is_borrowed = False


class Bookshelf():

    def __init__(self, lib_name):
        self.lib_name = lib_name
        self.books = []

    def add_book(self, book):
        self.books.append(book)
    
    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book) 
        else: 
            print("{} is not in the shelf".format(book.title))
    def list_books(self):
        print(self.__dict__)
        for book in self.books:
            print(book.__dict__)
    def search_by_author(self, author):
        for book in self.books:
            if book.author == author:
                print(book.__dict__)
    




shelf1 = Bookshelf("Babylon library")
for i in range(10):
    shelf1.add_book(Book("Book number {}".format(i), "Author number {}".format(i)))






shelf1.list_books()

