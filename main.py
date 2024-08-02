from fastapi import FastAPI

from database import init_tables
from router import router as date_router

app = FastAPI()
app.include_router(date_router)

# @app.on_event("startup")
# async def startup_event():
#     await init_tables()


if __name__ == '__main__':
    import uvicorn

    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)

