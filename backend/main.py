from fastapi import FastAPI
from app.routes import user_route, inventory_route

app = FastAPI(title="Ingrecipes API", version="1.0.0")
app.include_router(user_route.router)
app.include_router(inventory_route.router)

@app.get("/")
def read_root():
    return {"Message": "Welcome to the Ingrecipes API!"}
    