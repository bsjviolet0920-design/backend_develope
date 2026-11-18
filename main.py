# FastAPI 관련 기능
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# 데이터 형식 정의
from pydantic import BaseModel

# Firebase 데이터베이스 함수
from database import (
    get_user,
    create_user,
    update_user,
    verify_id_token
)

# FastAPI 앱 생성
app = FastAPI()

# Firebase 인증 방식 설정
security = HTTPBearer()

# ==========================================
# Firebase 로그인 사용자 인증
# ==========================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    # Bearer 토큰 가져오기
    token = credentials.credentials

    # Firebase ID Token 검증
    try:
        decoded_token = verify_id_token(token)
        return decoded_token

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="유효하지 않은 인증 토큰입니다."
        )


# 사용자 등록 시 받을 데이터 형식
class UserCreate(BaseModel):
    name: str


# 1. 서버 작동 확인
@app.get("/")
def home():
    return {"message": "Backend Server is Running!"}


# 2. 사용자 정보 조회
@app.get("/users/{user_id}")
def read_user(user_id: str):

    user = get_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="사용자를 찾을 수 없습니다."
        )

    return user


# 3. 사용자 정보 등록
@app.post("/users")
def register_user(
    user: UserCreate,
    current_user: dict = Depends(get_current_user)
):

    # Firebase ID Token에서 사용자 정보 가져오기
    uid = current_user["uid"]
    email = current_user.get("email")

    # 이미 등록된 사용자인지 확인
    if get_user(uid) is not None:
        raise HTTPException(
            status_code=409,
            detail="이미 등록된 사용자입니다."
        )

    # Firestore에 사용자 정보 저장
    new_user = create_user(
        user_id=uid,
        name=user.name,
        email=email
    )

    return {
        "message": "사용자 등록 성공!",
        "user": new_user
    }


# ==========================================
# 5. 로그인한 사용자 본인 정보 조회
# ==========================================

@app.get("/me")
def read_my_info(current_user: dict = Depends(get_current_user)):

    # Firebase ID Token에서 UID 가져오기
    uid = current_user["uid"]
    print("FastAPI가 받은 UID:", uid)
    print("인증 정보:", current_user)

    # UID를 이용해 Firestore에서 사용자 정보 조회
    user = get_user(uid)
    print("현재 인증된 UID:", uid)
    print("조회 결과:", user)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="사용자 정보가 등록되어 있지 않습니다."
        )

    return {
        "uid": uid,
        "user": user
    }


# ==========================================
# 4. 사용자 정보 수정
# ==========================================

@app.patch("/users/{user_id}")
def edit_user(user_id: str, update_data: dict):

    updated_user = update_user(user_id, update_data)

    if updated_user is None:
        raise HTTPException(
            status_code=404,
            detail="사용자를 찾을 수 없습니다."
        )

    return {
        "message": "사용자 정보 수정 성공!",
        "user": updated_user
    }

