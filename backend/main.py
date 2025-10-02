from fastapi import FastAPI

app = FastAPI(title="Ingrecipes API", version="1.0.0")

@app.get("/")
def read_root():
    return {"Message": "Welcome to the Ingrecipes API!"}
    