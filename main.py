import json
import os
import sys

# --- 1. THE BLUEPRINT (Book Class) ---
class Book:
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status

    def issue(self):
        if self.status == "available":
            self.status = "issued"
            return True
        return False

    def return_book(self):
        self.status = "available"

    def to_dict(self):
        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "status": self.status
        }

    def __str__(self):
        # Returns: [AVAILABLE] Harry Potter by J.K. Rowling (ISBN: 123)
        return f"[{self.status.upper()}] {self.title} by {self.author} (ISBN: {self.isbn})"


# --- 2. THE CONTROLLER (Inventory Manager) ---
class LibraryInventory:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = []
        self.load_data()

    def add_book(self, title, author, isbn):
        if self.get_book_by_isbn(isbn):
            print(f"Error: Book with ISBN {isbn} already exists.")
            return
        new_book = Book(title, author, isbn)
        self.books.append(new_book)
        self.save_data()
        print(f"Success: Added '{title}'")

    def search_by_title(self, query):
        # Linear search: check every book
        found_books = []
        for book in self.books:
            if query.lower() in book.title.lower():
                found_books.append(book)
        return found_books

    def get_book_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        if not self.books:
            print(" -- Inventory is empty --")
        for book in self.books:
            print(book)

    def save_data(self):
        data = [book.to_dict() for book in self.books]
        try:
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        # Remove the 'if exists' check. Just try to open it.
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.books = [Book(d['title'], d['author'], d['isbn'], d['status']) for d in data]
                print(f"Loaded {len(self.books)} books from storage.")
        except FileNotFoundError:
            print("WARNING: 'library.json' not found. Starting with empty inventory.")
            self.books = []
        except json.JSONDecodeError:
            print("ERROR: 'library.json' is corrupted. Starting empty.")
            self.books = []


# --- 3. THE INTERFACE (Void Loop) ---
def main():
    manager = LibraryInventory()

    while True:
        print("\n=== LIBRARY MENU ===")
        print("1. Add Book")
        print("2. List All Books")
        print("3. Search by Title")
        print("4. Issue Book")
        print("5. Return Book")
        print("6. Exit")
        
        choice = input("Enter choice: ")

        if choice == '1':
            t = input("Title: ")
            a = input("Author: ")
            i = input("ISBN: ")
            manager.add_book(t, a, i)

        elif choice == '2':
            manager.display_all()

        elif choice == '3':
            q = input("Search Title: ")
            results = manager.search_by_title(q)
            for book in results:
                print(book)

        elif choice == '4':
            i = input("Enter ISBN to Issue: ")
            book = manager.get_book_by_isbn(i)
            if book:
                if book.issue():
                    manager.save_data() # SAVE STATE AFTER CHANGE!
                    print("Book Issued Successfully.")
                else:
                    print("Error: Book is already issued.")
            else:
                print("Book not found.")

        elif choice == '5':
            i = input("Enter ISBN to Return: ")
            book = manager.get_book_by_isbn(i)
            if book:
                book.return_book()
                manager.save_data() # SAVE STATE!
                print("Book Returned.")
            else:
                print("Book not found.")

        elif choice == '6':
            print("Goodbye!")
            break
        
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()