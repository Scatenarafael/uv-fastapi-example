from typing import List, Union

from fastapi import FastAPI, HTTPException, responses, status
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
        get_items = [
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "is_offer": item.is_offer,
            }
            for item in items
        ]
        return responses.JSONResponse(
            status_code=status.HTTP_200_OK, content={"items": get_items}
        )
    except Exception as e:
        print("Error trying to list items:", e)
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


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
        print("Item created:", item)
        return responses.JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "item": {
                    "id": item.id,
                    "name": item.name,
                    "price": item.price,
                    "is_offer": item.is_offer,
                }
            },
        )
    except Exception as e:
        print("Error trying to create item:", e)
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        )


@app.get("/items/{item_id}")
def retrieve_item(item_id: int):
    filtered_items = [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "is_offer": item.is_offer,
        }
        for item in items
        if item.id == item_id
    ]

    if not filtered_items:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    return responses.JSONResponse(
        status_code=status.HTTP_200_OK, content=filtered_items[0]
    )


@app.put("/items/{item_id}")
def update_item(item_id: int, body: PartialItem):
    try:
        filtered_items = [item for item in items if item.id != item_id]
        selected_item = [item for item in items if item.id == item_id]

        print("Selected item:", selected_item)
        print("Filtered items:", filtered_items)

        if not selected_item:
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )

        for key, value in body.model_dump(exclude_unset=True).items():
            setattr(selected_item[0], key, value)

        filtered_items.append(selected_item[0])
        items.clear()
        items.extend(filtered_items)
        return responses.JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "item": {
                    "id": item_id,
                    "name": selected_item[0].name,
                    "price": selected_item[0].price,
                    "is_offer": selected_item[0].is_offer,
                }
            },
        )
    except Exception as e:
        print("Error trying to update item:", e)
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    try:
        filtered_items = [item for item in items if item.id != item_id]

        items.clear()
        items.extend(filtered_items)
        return responses.JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Item deleted successfully"},
        )
    except Exception as e:
        print("Error trying to delete item:", e)
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
