from fastapi import FastAPI

# FastAPI 앱 생성
app = FastAPI()

# 첫 번째 API
@app.get("/")
def home():
    return {"message": "Backend Server is Running!"}