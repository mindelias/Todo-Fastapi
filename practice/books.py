from fastapi import FastAPI, Body
app = FastAPI()


books = [
    {
        "name": "book1",
        "author": "author1",
        "category": "history"
    },
    {
        "name": "book2",
        "author": "author2",
        "category": "science"
    },
    {
        "name": "book3",
        "author": "author3",
        "category": "science"
    },
    {
        "name": "book4",
        "author": "author4",
        "category": "maths"
    },
    {
        "name": "book5",
        "author": "author1",
        "category": "arts"
    },
    {
        "name": "book6",
        "author": "author6",
        "category": "arts"
    }

]
    

@app.get("/books")
async def get_books():
    return books

@app.get("/books/{book_name}")
async def get_book(book_name: str):
    # return [book for book in books if book["name"] == book_name]
    for book in books:
        if book.get("name").casefold() == book_name.casefold():
            return book

    return {"data": "not found"}

@app.get("/books/category/")
async def get_book_by_category(category: str):
    books_to_return = []
    # books_to_return = [book for book in books if book.get("category", "").casefold() == category.casefold()]
    for book in books:
        if book.get("category", "").casefold() == category.casefold():
            books_to_return.append(book)

    return {"data": books_to_return}

@app.get("/books/{author}/")
async def get_book_by_author_categpry(author: str, category):
      
     books_to_return = [book for book in books if book.get("author", "").casefold() == author.casefold() and \
                        book.get("category", "").casefold() == category.casefold()]

     
     return books_to_return


@app.post("/books/create_book")
async def create_book(book: dict):
    books.append(book)
    return book


@app.put("/books/update_book")
async def update_book(payload: dict = Body(...)):
     
    for book in books:
        if(book.get("name").casefold() == payload.get("name").casefold()):
            book.update(payload) 
            return {"message": "Book updated", "data": book}

    return {"message": "Book not found"}




