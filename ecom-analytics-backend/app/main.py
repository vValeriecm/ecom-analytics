from fastapi import FastAPI

app = FastAPI(title="E-commerce Analytics API")

@app.get("/")
async def root():
    return {"message": "Welcome to E-commerce Analytics API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
