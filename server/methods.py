import os
from fastapi import UploadFile


async def save_image(order_number: int, image: UploadFile):
    image_data = await image.read()
    image_path = f'images/{order_number}.jpg'
    os.makedirs('images', exist_ok=True)
    with open(image_path, 'wb') as f:
        f.write(image_data)
    return image_path