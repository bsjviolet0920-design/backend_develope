
# ==========================================
# database.py
# Firebase Firestore 연결 및 데이터베이스 관리
# ==========================================

import os
from pathlib import Path

import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
from firebase_admin import auth


# 1. 프로젝트 기본 경로
BASE_DIR = Path(__file__).resolve().parent


# 2. .env 파일 불러오기
load_dotenv(BASE_DIR / ".env")


# 3. Firebase 비공개 키 경로 가져오기
key_path = os.getenv("FIREBASE_KEY_PATH")

if not key_path:
    raise ValueError("Firebase 키 경로가 설정되지 않았습니다.")

KEY_PATH = BASE_DIR / key_path


# 4. Firebase 초기화
if not firebase_admin._apps:
    cred = credentials.Certificate(str(KEY_PATH))
    firebase_admin.initialize_app(cred)


# 5. Firestore 데이터베이스 연결
db = firestore.client()


# 6. 컬렉션 참조
users_collection = db.collection("users")
places_collection = db.collection("places")
stamps_collection = db.collection("stamps")
reviews_collection = db.collection("reviews")
inquiries_collection = db.collection("inquiries")
festivals_collection = db.collection("festivals")


print("Firebase Firestore 연결 성공!")


# ==========================================
# 사용자 데이터 저장
# ==========================================

def create_user(user_id, name, email):
    user_data = {
        "name": name,
        "email": email,
        "role": "user",
        "stamp_count": 0
    }

    users_collection.document(user_id).set(user_data)

    return user_data


# ==========================================
# 사용자 데이터 조회
# ==========================================

def get_user(user_id):
    print("조회하려는 문서 ID:", user_id)

    user_doc = users_collection.document(user_id).get()

    print("문서 존재 여부:", user_doc.exists)

    if user_doc.exists:
        return user_doc.to_dict()

    return None
print("UID 문서 직접 조회 테스트")

test_doc = users_collection.document("PV6y3M2l5rRlLULMs4RitJC6pUi2").get()

print("문서 존재 여부:", test_doc.exists)
print("문서 데이터:", test_doc.to_dict())

# ==========================================
# 사용자 정보 수정
# ==========================================

def update_user(user_id, update_data):
    user_doc = users_collection.document(user_id)

    # 사용자가 존재하는지 확인
    if not user_doc.get().exists:
        return None

    # 전달받은 정보만 수정
    user_doc.update(update_data)

    # 수정된 사용자 정보 반환
    return user_doc.get().to_dict()

# ==========================================
# Firebase ID Token 검증
# ==========================================

def verify_id_token(id_token):
    decoded_token = auth.verify_id_token(id_token)

    return decoded_token

print("Firebase 프로젝트 ID:", firebase_admin.get_app().project_id)

print("users 컬렉션 문서 목록:")

for doc in users_collection.stream():
    print("문서 ID:", doc.id)
    print("문서 데이터:", doc.to_dict())