from database import create_user, get_user

# 1. 사용자 정보 저장하기
create_user(
    user_id="test_user_001",
    name="홍길동",
    email="test@test.com"
)

print("사용자 등록 완료!")

# 2. 저장한 사용자 정보 다시 가져오기
user = get_user("test_user_001")

print("조회된 사용자 정보:")
print(user)