from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

db: dict[int, Item] = {
    1: Item(id=1, name="Laptop", description="A high-performance laptop for development", price=100.99),
    2: Item(id=2, name="Mouse", description="Wireless ergonomic mouse", price=15.95),
    3: Item(id=3, name="Keyboard", price=23.45, tax=3.54),
}

@app.post("/item")
async def item_post(item: Item):
    item_dict = item.model_dump()
    if item_dict.id in db:
        raise HTTPException(status_code=409, detail="Item already exists")
    if item_dict.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    db[item_dict.id] = item_dict
    return item_dict


@app.get("/item")
async def get_item(item: Item):
    item_dict = item.model_dump()
    return item_dict

@app.get("/item/{item_id}")
async def get_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
