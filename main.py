from typing import List, Union

from fastapi import FastAPI
from pydantic import BaseModel

# from sqlmodel import Field

app = FastAPI()


class Item(BaseModel):
    id: Union[int, None] = None
    name: str
    price: float
    is_offer: Union[bool, None] = False


class PartialItem(BaseModel):
    id: Union[int, None] = None
    name: Union[str, None] = None
    price: Union[float, None] = None
    is_offer: Union[bool, None] = None


items: List[Item] = []


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def list_items():
    try:
        get_items = [item for item in items]
    except Exception as e:
        print("Error trying to list items:", e)
        return {"error": str(e)}
    return {"items": get_items}


@app.post("/items")
def create_item(item: Item):
    try:
        if not items:
            item.id = 1
        else:
            max_item_id = max(
                [item.id for item in items if item.id is not None]
            )
            item.id = max_item_id + 1
        items.append(item)
    except Exception as e:
        print("Error trying to create item:", e)
        return {"error": str(e)}
    return {"item_name": item.name, "item_price": item.price}


@app.get("/items/{item_id}")
def retrieve_item(item_id: int):
    filtered_items = [item for item in items if item.id == item_id]

    if not filtered_items:
        return {"detail": "Item not found"}
    return {"item_id": filtered_items[0]}


@app.put("/items/{item_id}")
def update_item(item_id: int, body: PartialItem):
    try:
        filtered_items = [item for item in items if item.id != item_id]
        selected_item = [item for item in items if item.id == item_id]

        if not selected_item:
            return {"detail": "Item not found"}

        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(selected_item[0], key, value)

        filtered_items.append(selected_item)
        items.clear()
        items.extend(filtered_items)
        return {"item": selected_item}
    except Exception as e:
        print("Error trying to update item:", e)
        return {"error": str(e)}
