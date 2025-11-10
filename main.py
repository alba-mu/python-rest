from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated

app = FastAPI()

# Model Pydantic
class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

# Base de dades simulada
db: dict[int, Item] = {
    1: Item(id=1, name="Laptop", description="A high-performance laptop for development", price=100.99),
    2: Item(id=2, name="Mouse", description="Wireless ergonomic mouse", price=15.95),
    3: Item(id=3, name="Keyboard", price=23.45, tax=3.54),
}


# Crear un nou item
@app.post("/item", response_model=Item)
async def create_item(item: Item):
    if item.id in db:
        raise HTTPException(status_code=409, detail="Item already exists")

    db[item.id] = item
    return item


# Obtenir tots els items
@app.get("/item", response_model=list[Item])
async def get_all_items():
    return list(db.values())


# Obtenir un item per id
@app.get("/item/{item_id}", response_model=Item)
async def get_item_by_id(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")

    return db[item_id]
