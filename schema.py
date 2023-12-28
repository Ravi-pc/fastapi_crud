from pydantic import BaseModel, Field, EmailStr


class Contact(BaseModel):
    book_name: str
    first_name: str
    last_name: str
    pin: int
    email: EmailStr
    city: str
    state: str

