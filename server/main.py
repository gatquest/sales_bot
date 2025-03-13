from fastapi import FastAPI
from api import router
import uvicorn

app = FastAPI()

# Подключение маршрутов
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
