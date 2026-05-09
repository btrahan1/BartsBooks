import os

books_dir = r"C:\Users\bartt\Projects\BartsBooks\books"
total_words = 0

for book_folder in os.listdir(books_dir):
    book_path = os.path.join(books_dir, book_folder)
    if os.path.isdir(book_path):
        for file in os.listdir(book_path):
            if file.endswith(".md") and file != "synopsis.md" and file != "notes.md":
                file_path = os.path.join(book_path, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    words = content.split()
                    total_words += len(words)

print(f"Total word count across all books: {total_words}")
