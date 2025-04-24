import json


class BookCollection:
    def __init__(self):
        self.book_list = []
        self.storage_file = "books_data.json"
        self.read_from_file()

    def read_from_file(self):
        try:
            with open(self.storage_file, "r") as file:
                self.book_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.book_list = []

    def save_to_file(self):
        with open(self.storage_file, "w") as file:
            json.dump(self.book_list, file, indent=4)

    def get_input(self, prompt, default=None):
        """Input wrapper to allow default value fallback."""
        user_input = input(prompt).strip()
        return user_input if user_input else default

    def create_new_book(self):
        book_title = self.get_input("Enter book title: ")
        if any(book["title"].lower() == book_title.lower() for book in self.book_list):
            print("This book already exists in the collection.\n")
            return

        book_author = self.get_input("Enter author: ")

        while True:
            publication_year = self.get_input("Enter publication year: ")
            if publication_year.isdigit():
                break
            print("Please enter a valid year.")

        book_genre = self.get_input("Enter genre: ")
        is_book_read = self.get_input("Have you read this book? (yes/no): ").lower() == "yes"

        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
        }

        self.book_list.append(new_book)
        self.save_to_file()
        print("Book added successfully!\n")

    def delete_book(self):
        book_title = self.get_input("Enter the title of the book to remove: ")
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                self.book_list.remove(book)
                self.save_to_file()
                print("Book removed successfully!\n")
                return
        print("Book not found!\n")

    def find_book(self):
        search_type = self.get_input("Search by:\n1. Title\n2. Author\nEnter your choice: ")
        search_text = self.get_input("Enter search term: ").lower()
        
        if search_type == "1":
            found_books = [book for book in self.book_list if search_text in book["title"].lower()]
        elif search_type == "2":
            found_books = [book for book in self.book_list if search_text in book["author"].lower()]
        else:
            print("Invalid option.\n")
            return

        if found_books:
            print("Matching Books:")
            for index, book in enumerate(found_books, 1):
                status = "Read" if book["read"] else "Unread"
                print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {status}")
        else:
            print("No matching books found.\n")

    def update_book(self):
        book_title = self.get_input("Enter the title of the book you want to edit: ")
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                print("Leave blank to keep existing value.")
                book["title"] = self.get_input(f"New title ({book['title']}): ", book["title"])
                book["author"] = self.get_input(f"New author ({book['author']}): ", book["author"])
                book["year"] = self.get_input(f"New year ({book['year']}): ", book["year"])
                book["genre"] = self.get_input(f"New genre ({book['genre']}): ", book["genre"])
                read_input = self.get_input("Have you read this book? (yes/no): ").lower()
                if read_input in ["yes", "no"]:
                    book["read"] = read_input == "yes"
                self.save_to_file()
                print("Book updated successfully!\n")
                return
        print("Book not found!\n")

    def show_all_books(self):
        if not self.book_list:
            print("Your collection is empty.\n")
            return

        print("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            print(f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
        print()

    def show_reading_progress(self):
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (completed_books / total_books * 100) if total_books else 0
        print(f"Total books in collection: {total_books}")
        print(f"Books read: {completed_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")

    def export_books(self):
        export_file = self.get_input("Enter export filename (default: exported_books.json): ", "exported_books.json")
        with open(export_file, "w") as f:
            json.dump(self.book_list, f, indent=4)
        print(f"Books exported to {export_file}\n")

    def start_application(self):
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View reading progress")
            print("7. Export book collection")
            print("8. Exit")
            user_choice = self.get_input("Please choose an option (1-8): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.export_books()
            elif user_choice == "8":
                self.save_to_file()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()
