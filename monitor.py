import requests
from bs4 import BeautifulSoup
import os

# 봇 정보 설정
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TARGET_URL = "https://www.reum.kr/user/pbas/list"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.get(url, params=params)

def check_site():
    try:
        # 1. 사이트 접속 및 데이터 가져오기
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(TARGET_URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 2. 상세 페이지로 연결되는 최신 링크(pbasCd) 찾기
        first_item = soup.select_one('a[href*="detail/?pbasCd="]')
        
        if not first_item:
            print("목록을 읽어오지 못했습니다.")
            return

        # 글 번호(ID) 추출 (예: 20260327001)
        current_id = first_item['href'].split('=')[-1]
        detail_url = f"https://www.reum.kr/user/pbas/detail/?pbasCd={current_id}"

        # 3. 이전 기록장(last_id.txt)과 비교
        if os.path.exists('last_id.txt'):
            with open('last_id.txt', 'r') as f:
                last_id = f.read().strip()
        else:
            last_id = ""

        # 4. 새 글이면 알림 보내고 기록 업데이트
        if current_id != last_id:
            msg = f"🔔 *[보험잔존물] 새로운 매물 등록!*\n\n🔗 [상세보기 클릭]({detail_url})"
            send_telegram(msg)
            with open('last_id.txt', 'w') as f:
                f.write(current_id)
            print(f"새 글 알림 발송 완료: {current_id}")
        else:
            print("업데이트된 새 글이 없습니다.")
            
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_site()
