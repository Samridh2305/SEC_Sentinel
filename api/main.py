from fastapi import FastAPI

app = FastAPI(title="SEC Sentinel")


@app.get("/")
def root():
    return {"message": "SEC Sentinel API is running"}