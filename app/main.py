from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health_status():
    return {"status": "ok"}