from fastapi import FastAPI

app=FastAPI()

BOOKS = [
    {'tiltle':'Title One', 'author': 'Author One', 'category': 'science'},
    {'tiltle':'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'tiltle':'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'tiltle':'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'tiltle':'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'tiltle':'Title Six', 'author': 'Author Six', 'category': 'math'}
    
]



@app.get('/books')
async def read_all_books():
    return BOOKS