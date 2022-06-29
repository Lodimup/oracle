from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():

    rdb = .....

    return {"message": "Hello World"}
