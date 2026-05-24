from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


app=FastAPI()

@app.get("/")
def home():
    return {"home"}