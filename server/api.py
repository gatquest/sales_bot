from fastapi import APIRouter, HTTPException, File, UploadFile, Form
from pydantic import ValidationError
from db import db_create_order, db_get_order, db_put_image_to_order, db_get_orders
from serialize import CreateOrder, GetOrder
import os
from pprint import pprint
from typing import Dict, List

from methods import save_image

router = APIRouter()



@router.get("/api/order/{order_number}")
async def api_get_order(order_number: int) -> Dict:
    item = db_get_order(order_number)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/api/orders")
async def api_get_orders() -> List[Dict]:
    item = db_get_orders()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/api/upload-form/")
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

