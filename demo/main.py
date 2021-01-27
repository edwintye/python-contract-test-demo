from typing import Optional

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()

items = dict()


async def get_item(item_id: int) -> Optional[Item]:
    if item_id in items:
        return items[item_id]
    else:
        return None


async def add_item(item_id: int, item: Item) -> Optional[Item]:
    if item_id in items:
        return None
    else:
        items[item_id] = item.dict()
        return items[item_id]


async def delete_item(item_id: int) -> Optional[bool]:
    if item_id in items:
        del items[item_id]
        return True
    else:
        return None


@app.get("/healthz")
async def get_health():
    return {"msg": "Healthy"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    res = await get_item(item_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return res


@app.put("/items/{item_id}", status_code=201)
async def create_item(item_id: int, item: Item):
    res = await add_item(item_id, item)
    if res is None:
        raise HTTPException(status_code=409, detail="Item exists")
    else:
        return res


@app.delete("/items/{item_id}", status_code=200)
async def remove_item(deleted: Optional[bool] = Depends(delete_item)):
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return {"msg": "Successful"}
