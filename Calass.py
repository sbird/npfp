# make a good code
# add init functions
# add class of book shelf
# function to add and remove book from shelf
# funcrtion to find book by author, year ...


class Book():

	def __init__(self):
	
		self.title = ""
		self.author = ""
		self.tags = []
		self.published_year = 0
		self.n_borrowed = 0
		self.last_borrowed = ""
		self.ISBN_13 = ""
		
		
	def add_book():
	def borrow_a_book(self):
	
class Bookshelf:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)
        print(f"Added book '{book}' to the bookshelf.")

    def remove_book(self, book):
        if book in self.books:
            self.books.remove(book)
            print(f"Removed book '{book}' from the bookshelf.")
        else:
            print(f"Book '{book}' not found on the bookshelf.")

    def find_books_by_author(self, author):
        found_books = []
        for book in self.books:
            if book.author == author:
                found_books.append(book)
        if found_books:
            print(f"Books by author '{author}':")
            for book in found_books:
                print(book)
        else:
            print(f"No books found by author '{author}'.")

    def find_books_by_year(self, year):
        found_books = []
        for book in self.books:
            if book.year == year:
                found_books.append(book)
        if found_books:
            print(f"Books published in year {year}:")
            for book in found_books:
                print(book)
        else:
            print(f"No books found published in year {year}.")


# Example usage
class Book:
    def __init__(self, title, author, year):
        self.title = title
        self.author = author
        self.year = year

    def __str__(self):
        return f"Book: {self.title} by {self.author} ({self.year})"


# Create a bookshelf instance
my_bookshelf = Bookshelf()

# Add books to the bookshelf
book1 = Book("Harry Potter and the Philosopher's Stone", "J.K. Rowling", 1997)
book2 = Book("To Kill a Mockingbird", "Harper Lee", 1960)
book3 = Book("1984", "George Orwell", 1949)

my_bookshelf.add_book(book1)
my_bookshelf.add_book(book2)
my_bookshelf.add_book(book3)

# Remove a book from the bookshelf
my_bookshelf.remove_book(book2)

# Find books by author
my_bookshelf.find_books_by_author("J.K. Rowling")

# Find books by year
my_bookshelf.find_books_by_year(1949)
