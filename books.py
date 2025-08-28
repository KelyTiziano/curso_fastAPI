from fastapi import FastAPI

app=FastAPI()

BOOKS = [
    {'title':'Title One', 'author': 'Author One', 'category': 'science'},
    {'title':'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title':'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title':'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title':'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title':'Title Six', 'author': 'Author Six', 'category': 'math'}
]



@app.get('/books')
async def read_all_books():
    return BOOKS

@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {'dynamic_param': dynamic_param}

@app.get("/calculo/{a}/{b}")
async def calcule_soma(a: int, b: int):
    return {'resultado': a + b}

@app.get("/books/")
async def read_title_by_query(title: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('title').casefold() == title.casefold():
            books_to_return.append(book)
    return books_to_return

@app.get("/livros/{book_author}")
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
           book.get('category').casefold() == category.casefold():
           books_to_return.append(book)
    return books_to_return
