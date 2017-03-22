books = {"Anish": ["Book1", "Book2", "Book3"], "Rob Roy": ["Awesome Book1"]}

books["Rob Roy"].append("Other Book")
books["Tom"] = ["Tom's First Book"]

def get_books(author):
    return books[author]

print(get_books("Anish"))

print("This author has written " + ", ".join(get_books("Anish")))


