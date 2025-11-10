from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from user import  *
from user import add_user

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Model Pydantic
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Base de dades simulada
db_item: dict[int, Item] = {
    1: Item(id=1, name="Laptop", description="A high-performance laptop for development", price=100.99),
    2: Item(id=2, name="Mouse", description="Wireless ergonomic mouse", price=15.95),
    3: Item(id=3, name="Keyboard", price=23.45, tax=3.54),
}


# Crear un nou item
@app.post("/item", response_model=Item)
async def create_item(item: Item):
    if item.id in db_item:
        raise HTTPException(status_code=409, detail="Item already exists")

    db_item[item.id] = item
    return item


# Obtenir tots els items
@app.get("/item", response_model=list[Item])
async def get_all_items():
    return list(db_item.values())


# Obtenir un item per id
@app.get("/item/{item_id}", response_model=Item)
async def get_item_by_id(item_id: int):
    if item_id not in db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    return db_item[item_id]



@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = db_user.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    hashed_password = db_user.get(form_data.password)
    if not authenticate(user_dict.id, user_dict.password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": token_create(user_dict.id), "token_type": "bearer"}


add_user(User("alba", "1234"))
