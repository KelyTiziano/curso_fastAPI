# Cria a aplicação FastAPI
# Body → permite receber dados JSON no corpo da requisição (usado em POST ou PUT).
from fastapi import Body, FastAPI

# 'app' será usada para registrar todas as rotas da API
# FastAPI() → cria a aplicação que vai responder às requisições HTTP.
app=FastAPI()

# Lista de livros disponíveis na API
# Cada livro é representado como um dicionário com os campos:
# - 'title' (str): título do livro
# - 'author' (str): nome do autor
# - 'category' (str): categoria ou área do livro

BOOKS = [
    {'title':'Title One', 'author': 'Author One', 'category': 'science'},
    {'title':'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title':'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title':'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title':'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title':'Title Six', 'author': 'Author Six', 'category': 'math'}
]
# Retorna a lista completa de livros disponíveis na API.
# Método: GET
# Rota: /books

@app.get('/books')
async def read_all_books():
    return BOOKS

# Retorna o valor recebido como parâmetro de caminho.
# Método: GET
# Rota: /books/{dynamic_param}
# Parâmetros: dynamic_param (str): valor passado na URL que será retornado na resposta.
# Retorno: dict: um dicionário contendo o parâmetro recebido
# Exemplo: {"dynamic_param": "exemplo"}

'''Observações:
Essa rota não acessa os livros, apenas retorna o valor que foi passado na URL.
Útil para testar parâmetros de caminho no FastAPI.'''

@app.get("/books/{dynamic_param}")
async def read_all_books(dynamic_param):
    return {'dynamic_param': dynamic_param}

"""
    Calcula a soma de dois números inteiros recebidos como parâmetros de caminho.

    Método: GET
    Rota: /calculo/{a}/{b}

    Parâmetros:
    - a (int): primeiro número
    - b (int): segundo número

    Retorno:
    - dict: um dicionário com o resultado da soma.
    Exemplo: {"resultado": 7} se a=3 e b=4
    """

@app.get("/calculo/{a}/{b}")
async def calcule_soma(a: int, b: int):
    return {'resultado': a + b}

"""
    Busca livros pelo título informado como parâmetro de consulta (query parameter).

    Método: GET
    Rota: /books/?title={nome_do_titulo}

    Parâmetros:
    - title (str): título do livro a ser buscado (não diferencia maiúsculas e minúsculas).

    Funcionamento:
    - Percorre a lista BOOKS.
    - Retorna uma lista contendo todos os livros que possuem o título igual ao informado.

    Retorno:
    - list: lista de dicionários com os livros encontrados.
    Exemplo de resposta:
    [
        {"title": "Title One", "author": "Author One", "category": "science"}
    ]
    """

@app.get("/books/")
async def read_title_by_query(title: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('title').casefold() == title.casefold():
            books_to_return.append(book)
    return books_to_return


    """
    Busca livros de um autor específico que pertençam a uma categoria informada.
 
    Método: GET  
    Rota: /livros/{book_author}?category={nome_da_categoria}  

    Parâmetros:
    - book_author (str) [Path]: nome do autor (não diferencia maiúsculas e minúsculas).
    - category (str) [Query]: categoria do livro (não diferencia maiúsculas e minúsculas).

    Funcionamento:
    - Percorre a lista BOOKS.
    - Compara se o autor do livro corresponde ao `book_author`.
    - Verifica também se a categoria do livro corresponde ao `category`.
    - Caso ambas condições sejam verdadeiras, adiciona o livro na lista de retorno.

    Retorno:
    - list: lista de dicionários contendo os livros encontrados.  
    Exemplo de resposta:
    [
        {"title": "Title Four", "author": "Author Four", "category": "math"}
    ]
    """

@app.get("/livros/{book_author}")
async def read_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
           book.get('category').casefold() == category.casefold():
           books_to_return.append(book)
    return books_to_return

"""
    Adiciona um novo livro à lista de livros (BOOKS).

    Método: POST  
    Rota: /books/create_book  

    Parâmetros:
    - new_book (Body): um dicionário JSON contendo as informações do livro.  
      Exemplo:
      {
          "title": "Novo Título",
          "author": "Novo Autor",
          "category": "Nova Categoria"
      }

    Funcionamento:
    - O endpoint recebe o novo livro pelo corpo da requisição.
    - Antes de adicionar, verifica se o autor NÃO é "kely".
    - Se o autor não for "kely", o livro é adicionado à lista BOOKS e a mensagem 
      "livro adicionado" é exibida no console.
    - Se o autor for "kely", o livro **não é adicionado** e a mensagem 
      "livro nao adicionado" é exibida.

    Retorno:
    - (nenhum retorno explícito, apenas modifica a lista BOOKS e imprime no console).

    Observação:
    - Na prática, seria interessante retornar um JSON de confirmação ao invés 
      de apenas `print` no console. Por exemplo:
      {"message": "Livro adicionado com sucesso"} ou {"message": "Livro não adicionado"}.
    """

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    if new_book.get('author').casefold() != "kely".casefold():
        print ('livro adicionado')
        BOOKS.append(new_book)
    else:
        print('livro nao adicionado')

"""
    Atualiza as informações de um livro existente na lista BOOKS.

    Método: PUT  
    Rota: /books/update_book  

    Parâmetros:
    - update_book (Body): um dicionário JSON contendo as informações atualizadas do livro.  
      O título ("title") é usado como chave para identificar o livro a ser atualizado.  

      Exemplo de JSON:
      {
          "title": "Title One",
          "author": "Novo Autor",
          "category": "Nova Categoria"
      }

    Funcionamento:
    - Percorre a lista BOOKS procurando um livro com o mesmo título informado.
    - Quando encontra, substitui o livro antigo pelos novos dados enviados.
    - Se não encontrar nenhum título correspondente, não faz nada.

    Retorno:
    - (nenhum retorno explícito, apenas modifica a lista BOOKS em memória).

    Observação:
    - Atualmente, o código não retorna nenhuma mensagem ao usuário.
    - Boa prática seria retornar algo como:
      {"message": "Livro atualizado com sucesso"} ou {"message": "Livro não encontrado"}.
    """

@app.put("/books/update_book")
async def update_book(update_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == update_book.get('title').casefold():
            BOOKS[i] = update_book

"""
    Deleta um livro da lista BOOKS pelo título.

    Método: DELETE  
    Rota: /books/delete_book/{book_title}  

    Parâmetros de caminho:
    - book_title (str): título do livro a ser deletado.  
      A comparação ignora diferenças entre maiúsculas e minúsculas.  

    Funcionamento:
    - Percorre a lista BOOKS.
    - Se encontrar um livro com o título correspondente, remove esse livro da lista.
    - Encerra a busca após remover o primeiro livro encontrado.
    - Se não encontrar, não faz nada (nenhuma mensagem é retornada atualmente).

    Retorno:
    - Nenhum retorno explícito (apenas altera a lista em memória).

    Observação:
    - Boa prática seria retornar uma resposta ao cliente, como:
      {"message": "Livro deletado com sucesso"} ou {"message": "Livro não encontrado"}.
    """

@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
    """
        Busca livros pelo autor.

        Método: GET  
        Rota: /books/search_author/  

        Parâmetros de consulta:
        - author (str): nome do autor a ser buscado.  
        A comparação ignora diferenças entre maiúsculas e minúsculas.  

        Funcionamento:
        - Cria uma lista vazia books_to_return.
        - Percorre todos os livros em BOOKS.
        - Se o autor do livro for igual ao parâmetro recebido, adiciona o livro na lista de retorno.
        - Retorna todos os livros que correspondem ao autor buscado.

        Retorno:
        - Lista de dicionários contendo os livros do autor pesquisado.
        - Se nenhum livro for encontrado, retorna uma lista vazia [].
    """

@app.get("/books/search_author/")
async def keep_author_by_query(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return
        