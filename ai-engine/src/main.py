import uvicorn
from fastapi import FastAPI

app = FastAPI(title="SupplyMind AI Engine")


@app.get("/")
def read_root():
    return {"status": "operational", "service": "SupplyMind AI Engine"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
