from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


# Book Class
class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


# BookRequest Class


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create.", default=None)
    title: str = Field(min_length=3)
    author: str = Field(
        pattern=r"^[A-Za-z]{2,}\s[A-Za-z]{2,}$",
        description="Two words, each at least 2 letters",
    )
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(gt=-1, lt=6)
    published_date: int = Field(gt=1999, lt=2026)

    # Set defaults for the BookRequest Class with model_config
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Timijobs",
                "description": "A new description of a book",
                "rating": 5,
                "published_date": 2020,
            }
        }
    }


BOOKS = [
    Book(
        1,
        "Ulysses",
        "James Joyce",
        "A stream-of-consciousness voyage through one day in Dublin.",
        5,
        1922,
    ),
    Book(
        2,
        "Lolita",
        "Vladimir Nabokov",
        "A haunting exploration of obsession and the limits of morality.",
        5,
        1955,
    ),
    Book(
        3,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "A tragic portrait of the American Dream set in the Jazz Age.",
        5,
        1925,
    ),
    Book(
        4,
        "Brave New World",
        "Aldous Huxley",
        "A chilling vision of a future society conditioned for conformity.",
        5,
        1932,
    ),
    Book(
        5,
        "Catch-22",
        "Joseph Heller",
        "Darkly comic tale of WWII airmen trapped by absurd bureaucracy.",
        5,
        1961,
    ),
    Book(
        6,
        "Moby-Dick",
        "Herman Melville",
        "An epic sea chase that probes the depths of obsession and revenge.",
        4,
        1851,
    ),
    Book(
        7,
        "War and Peace",
        "Leo Tolstoy",
        "A sweeping saga of Russian society during the Napoleonic Wars.",
        5,
        1869,
    ),
    Book(
        8,
        "The Adventures of Huckleberry Finn",
        "Mark Twain",
        "A boy’s raft journey down the Mississippi, exposing antebellum injustices.",
        5,
        1884,
    ),
    Book(
        9,
        "Middlemarch",
        "George Eliot",
        "A richly detailed portrait of provincial life and the intertwining fates of its citizens.",
        5,
        1872,
    ),
    Book(
        10,
        "Invisible Man",
        "Ralph Ellison",
        "A powerful story of identity and racism in mid-century America.",
        5,
        1952,
    ),
    Book(
        11,
        "Beloved",
        "Toni Morrison",
        "A searing novel of slavery’s legacy, haunted by the past and a restless spirit.",
        5,
        1987,
    ),
    Book(
        12,
        "Mrs. Dalloway",
        "Virginia Woolf",
        "A single day in post-WWI London, capturing one woman’s memories and reveries.",
        4,
        1925,
    ),
    Book(
        13,
        "One Hundred Years of Solitude",
        "Gabriel García Márquez",
        "A multi-generation tale of the Buendía family in the mythical town of Macondo.",
        5,
        1967,
    ),
    Book(
        14,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "An alienated teen’s journey through New York City and his own disillusionment.",
        4,
        1951,
    ),
    Book(
        15,
        "The Grapes of Wrath",
        "John Steinbeck",
        "A Dust Bowl family’s harrowing trek to California in search of dignity and work.",
        5,
        1939,
    ),
    Book(
        16,
        "The Sun Also Rises",
        "Ernest Hemingway",
        "A post-WWI “Lost Generation” story of love, bullfights, and expatriate disillusionment.",
        4,
        1926,
    ),
    Book(
        17,
        "Heart of Darkness",
        "Joseph Conrad",
        "A river voyage into the Congo that lays bare colonial brutality and moral decay.",
        5,
        1899,
    ),
    Book(
        18,
        "Frankenstein",
        "Mary Shelley",
        "A Gothic tale of creation and responsibility, pioneering science-fiction themes.",
        4,
        1818,
    ),
    Book(
        19,
        "Dracula",
        "Bram Stoker",
        "The classic vampire novel that melds horror, suspense, and Victorian anxieties.",
        4,
        1897,
    ),
    Book(
        20,
        "Crime and Punishment",
        "Fyodor Dostoevsky",
        "A tortured student’s moral struggle after committing a terrible deed.",
        5,
        1866,
    ),
]


@app.get("/books", status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.get("/books/publish", status_code=status.HTTP_200_OK)
async def read_by_published_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_books_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/create-book", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())  # .model_dump() for Pydantic 2
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    if len(BOOKS) > 0:
        book.id = BOOKS[-1].id + 1
    else:
        book.id = 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = Book(**book.model_dump())
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break
    if not book_deleted:
        raise HTTPException(status_code=404, detail="Item not found")
