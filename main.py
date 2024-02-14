import tkinter as tk
from tkinter import messagebox

class Library:
    def __init__(self, file_path):
        self.file_path = file_path

    def read_books(self):
        with open(self.file_path, "r") as file:
            books = [line.strip().split(",") for line in file.readlines()]
            return [{"title": book[0], "author": book[1]} for book in books]

    def add_book(self, book_info):
        with open(self.file_path, "a+") as file:
            file.write(f"{book_info['title']},{book_info['author']},{book_info['release_year']},{book_info['pages']}\n")

    def remove_book(self, title):
        with open(self.file_path, "r") as file:
            lines = file.readlines()
        with open(self.file_path, "w") as file:
            found = False
            for line in lines:
                if not line.startswith(title):
                    file.write(line)
                else:
                    found = True
            return found

class LibraryApp(tk.Tk):
    def __init__(self, file_manager):
        super().__init__()
        self.title("Library Management System")
        self.file_manager = file_manager

        self.frame_list = tk.Frame(self, padx=10, pady=10)
        self.frame_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.book_list = tk.Listbox(self.frame_list, width=50)
        self.book_list.pack(fill=tk.BOTH, expand=True)

        self.frame_input = tk.Frame(self, padx=10, pady=10)
        self.frame_input.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.label_title = tk.Label(self.frame_input, text="Title:")
        self.label_title.grid(row=0, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_title = tk.Entry(self.frame_input)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        self.label_author = tk.Label(self.frame_input, text="Author:")
        self.label_author.grid(row=1, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_author = tk.Entry(self.frame_input)
        self.entry_author.grid(row=1, column=1, padx=5, pady=5)

        self.label_release_year = tk.Label(self.frame_input, text="Release Year:")
        self.label_release_year.grid(row=2, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_release_year = tk.Entry(self.frame_input)
        self.entry_release_year.grid(row=2, column=1, padx=5, pady=5)

        self.label_pages = tk.Label(self.frame_input, text="Pages:")
        self.label_pages.grid(row=3, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_pages = tk.Entry(self.frame_input)
        self.entry_pages.grid(row=3, column=1, padx=5, pady=5)

        self.button_add = tk.Button(self.frame_input, text="Add Book", command=self.add_book)
        self.button_add.grid(row=4, column=0, columnspan=2, pady=5)

        self.label_remove = tk.Label(self.frame_input, text="Remove Book:")
        self.label_remove.grid(row=5, column=0, sticky=tk.E, padx=5, pady=5)
        self.entry_remove = tk.Entry(self.frame_input)
        self.entry_remove.grid(row=5, column=1, padx=5, pady=5)

        self.button_remove = tk.Button(self.frame_input, text="Remove", command=self.remove_book)
        self.button_remove.grid(row=6, column=0, columnspan=2, pady=5)

        self.button_quit = tk.Button(self.frame_input, text="Quit", command=self.quit)
        self.button_quit.grid(row=6, column=2, columnspan=2, pady=5)

        self.button_quit = tk.Button(self.frame_input, text="Add List", command=self.list_books)
        self.button_quit.grid(row=4, column=2, columnspan=2, pady=5)


    def list_books(self):
        books = self.file_manager.read_books()
        self.book_list.delete(0, tk.END)
        for book in books:
            self.book_list.insert(tk.END, f"Book: {book['title']},  Author: {book['author']}")

    def add_book(self):
        title = self.entry_title.get()
        author = self.entry_author.get()
        release_year = self.entry_release_year.get()
        pages = self.entry_pages.get()
        if title and author and release_year and pages:
            book_info = {"title": title, "author": author, "release_year": release_year, "pages": pages}
            self.file_manager.add_book(book_info)
            self.list_books()
            self.entry_title.delete(0, tk.END)
            self.entry_author.delete(0, tk.END)
            self.entry_release_year.delete(0, tk.END)
            self.entry_pages.delete(0, tk.END)

    def remove_book(self):
        title = self.entry_remove.get()
        if title:
            if not self.file_manager.remove_book(title):
                messagebox.showwarning("Book Not Found", f"Book '{title}' is not found.")
            else:
                self.list_books()
            self.entry_remove.delete(0, tk.END)

    def quit(self):
        self.destroy()

lib = Library("books.txt")
app = LibraryApp(lib)
app.mainloop()
