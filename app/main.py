from fastapi import FastAPI


app = FastAPI(title="Task Tracker API", description="Task Tracker API", version="1.0.0")



@app.get("/")
def home():
    return {"message": "FastAPI Task Tracker Running!"}