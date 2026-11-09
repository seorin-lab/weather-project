import os
import requests
from urllib.parse import unquote   # Encoding된 키를 원래 형태로 되돌리는 함수
from dotenv import load_dotenv

# .env 파일에서 인증키 불러오기 (코드에 키를 직접 쓰지 않음)
load_dotenv()
api_key = unquote(os.getenv("KMA_API_KEY"))

# ASOS 일자료 조회서비스 주소
url = "http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList"

# 요청 조건: 서울(108) 관측소의 2026년 11월 1일~7일 일자료
params = {
    "serviceKey": api_key,   # 인증키
    "pageNo": 1,             # 페이지 번호
    "numOfRows": 10,         # 한 번에 받을 행 수
    "dataType": "JSON",      # 응답 형식
    "dataCd": "ASOS",        # 자료 분류: 종관기상관측
    "dateCd": "DAY",         # 날짜 분류: 일자료
    "startDt": "20261101",   # 시작일
    "endDt": "20261107",     # 종료일
    "stnIds": "108",         # 관측소 번호 (108 = 서울)
}

response = requests.get(url, params=params)

# 응답이 JSON이 아니면 (키 오류 등) 원문을 그대로 출력해서 원인 확인
try:
    data = response.json()
except ValueError:
    print("JSON이 아닌 응답이 왔어요. 원문:")
    print(response.text)
    raise SystemExit

# 결과 코드 확인 ("00"이면 정상)
header = data["response"]["header"]
print("결과 코드:", header["resultCode"], header["resultMsg"])

# 날짜별 평균·최저·최고 기온과 강수량 출력
items = data["response"]["body"]["items"]["item"]
for item in items:
    print(
        item["tm"],                  # 날짜
        item["stnNm"],               # 관측소 이름
        "평균", item["avgTa"],        # 평균기온(°C)
        "최저", item["minTa"],        # 최저기온(°C)
        "최고", item["maxTa"],        # 최고기온(°C)
        "강수", item["sumRn"] or "0"  # 일강수량(mm), 비가 안 오면 빈 값
    )