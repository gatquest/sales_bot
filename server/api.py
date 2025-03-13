from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import ValidationError
from db import db_create_order, db_get_order, db_put_image_to_order 
from serialize import CreateOrder, GetOrder
import os

from methods import save_image

router = APIRouter()



@router.get("/orders/{order_number}")
async def api_get_order(order_number: int):
    item = db_get_order(order_number)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/upload-form/")
async def api_create_order(
    image: UploadFile = File(...),
    to_russia: str = Form(...),  # Поле для текстового описания
    size: str = Form(...),  # Поле для текстового описания
    price: str = Form(...),  # Поле для текстового описания
    client_name: str = Form(...),  # Поле для текстового описания

):
    
    # create order in db
    data = CreateOrder(
        to_russia=to_russia,
        size=size,
        price=price,
        client_name=client_name)
    try:
        new_order = db_create_order(data)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    image_path = await save_image(new_order, image)

    if image_path:
        await db_put_image_to_order(new_order, image_path)
        return {
            "message": f"Image and description uploaded successfully, order number: {new_order}"
        }
    else:
        return {
            "message": f"Failed to upload image, order number: {new_order}"
        }
        

# ... другие маршруты ...

