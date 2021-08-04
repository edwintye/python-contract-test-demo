from typing import Dict, Optional, Union

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

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


@router.get("/{item_id}")
async def read_item(item_id: int):
    res = await get_item(item_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return res


@router.put("/{item_id}", status_code=201)
async def create_item(item_id: int, item: Item):
    res = await add_item(item_id, item)
    if res is None:
        raise HTTPException(status_code=409, detail="Item exists")
    else:
        return res


@router.delete("/{item_id}", status_code=200)
async def remove_item(deleted: Optional[bool] = Depends(delete_item)):
    if deleted is None:
        raise HTTPException(status_code=404, detail="Item not found")
    else:
        return {"msg": "Successful"}