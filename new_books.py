'''
O pydantic é uma biblioteca python que ajuda a validar e organizar dados.
Ele garante que os dados que entram na sua aplicação tenham o tipo correto(str,int,list)
Tbm permite definir regras adicionais como tam minimo de uma str, valores max, min ou permitidos,
se o campo é opcioal, entre outros.

No fastAPI o pydantic é utilizado principalmente para validar dados que o usuario envia nas 
requisições, como no corpo de uma requisição POST.
___________________________________________________________________________________________________________
BaseModel Quando vc cria uma classe que herda de basemodel, vc diz que essa classe vai representar
dados que chegam ou saem da minha API, e quero que o pydantic valide esses dados automaticamente.
Se alguem enviar o tipo errado o fastAPI retorna um erro automatico.

Field serve para definir regras adicionais e specíficAS, para além do tipo, para cada campo do basemodel, 
como tamanho min ou max, valores permitidos, etc.
''' 

#Basemodel e Field: do pydantic, usados para validar dados de entrada e definir regras para os campos

from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException, status  #FastAPI classe principal que cria aplicação web
from pydantic import BaseModel, Field #Basemodel e Field: do pydantic, usados para validar dados de entrada e definir regras para os campos

app = FastAPI()#cria uma isntancia da classe FastAPI, isso é um lugar que guarda TUDO sobre sua aplicação web
#essa variavel é necessaria para a criação do seu fastAPI, sem isso nao consguimos nem rodar no servidor, é o coração da aplicação!

class Book: #classe Book define uma classe python, que é como um molde para criar objetos que representam livros, abaixo tem as anotações que 
    id: int #ajudam o python a entender os tipos, mas nao criam atributos automaticamente, isso acontece no init
    title: str
    author: str
    description: str
    rating: int
    published_date: int

#init é chamado automaticamente quando vc cria um objeto da classe Book
#Os parametros sao usados para inicializar os atributos do objeto
#self = referencia ao proprio objeto que esta sendo criado
#self.objeto atribui o valor do parametro objeto ao atributo objeto
    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

#Não entendi bem esse a parte do default
#A classe Book sozinha nao valida nada, é necessario usar Bookrequest do pydantic
# para validar os dados antes de criar o objeto
#Essa classe serve como modelo interno da aplicação, todos os livros criados via POST 
#ou adc a lista BOOKS são ojetos dessa classe
class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on creat', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)  
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2031)


    '''
    Não entendi bem! 
    Essa parte serve para fornecer exemplos para documentação automática do FastAPI (Swagger).
    Quando você abre /docs no navegador, aparece esse exemplo preenchido nos campos de criação do livro.
    '''

    model_config = {
        "json_schema_extra": { 
            "example": {
                "title": "A new book",
                "author": "codingwithroby",
                "description": "A new description of a book",
                "rating": 5 ,
                "published_date": 2029
            }
        }
    }
#BOOKS é uma lista python que serve como banco de dados temporario da aplicação, cada item da lista é um objeto da classe Book
#Todas as rotas GET acessam essa lista para retornar o titulo
#A rota POST adc novos livros a esta lista usando BOOKD.append(...)

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2000),
    Book(2, 'Be fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2025),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 1999),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2001),
    Book(5, 'HP2', 'Author 2', 'Book Description!', 3, 2029),
    Book(6, 'HP3', 'Author 3', 'Book Description!', 1, 2012)
]

@app.get("/books", status_code=status.HTTP_200_OK) #@ é um decorator que junta a função em uma rota da api
async def read_all_books():#async permite que essa função rode de forma assincrona, entre varias outras requisições sem travar, a funçao nao tem parametro e vai rodar o que vier abaixo
    return BOOKS #retorna a lista BOOKS

#essa rota permite buscar um book especifico pelo seu ID
@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)#{}significa que o texto do parametro é dinamico e pode mudar. COMO ASSIM?
async def read_book(book_id: int= Path(gt=0)):#função com parametro q sera convertido para inteiro, se colocar algo diferente dará um erro
    for book in BOOKS:#percorre todos os books da lista
        if book.id == book_id:#verifica se o id do book é igual ao id passado na url 
            return book#se encontrar esse ID retorna esse book 
    raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=6)):#Função será executada quando chamarem a rota /books/;Ela espera receber um parâmetro chamado book_rating = int, ele é passado na url após um ?(sinal de ?)
    books_to_return = []#cria uma lista vazia       
    for book in BOOKS:#percorre cada book in BOOKS
        if book.rating == book_rating:#se o book.rating for igual ao valor recebido no parametro na url
            books_to_return.append(book)#add esse book encontrado na lista que estava vazia
    return books_to_return #retorna a lista de livros filtrados


@app.post("/create-book", status_code=status.HTTP_201_CREATED)#rota post usada para enviar dados
async def create_book(book_request: BookRequest):#esse parametro significa que o corpo da função deve seguir o modelo bookRequest;o fastAPI vai usar o Pydantic para validar os dados automaticamente
    new_book = Book(**book_request.dict())#nao consegui entender
    BOOKS.append(find_book_id(new_book))#antes de adicionar o new book a lista BOOK, a função é chamada para garantir que o ID do book seja unico e sequencial

def find_book_id(book: Book):#não entendi essa função
    
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    
    '''if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1'''
    return book 

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book:BookRequest):
    book_changed = False 
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_change = True 
    if not book_changed: 
        raise HTTPException(status_code=204, detail='Item not found')

@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break 
    if not book_changed: 
        raise HTTPException(status_code=404, detail='Item not found')

@app.get("/books/publish", status_code=status.HTTP_200_OK)
async def read_books_by_publish_date (published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []      
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return 