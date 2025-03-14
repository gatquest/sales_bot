from fastapi import FastAPI
from api import router
import uvicorn
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Подключение маршрутов
app.include_router(router)

# Монтируем папку с изображениями как статический ресурс
app.mount("/images", StaticFiles(directory="images"), name="images")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
