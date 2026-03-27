import requests
from bs4 import BeautifulSoup
import os

# 금고(Secrets)에서 꺼내오는 정보
TOKEN = os.environ['TELEGRAM_TOKEN']
CHAT_ID = os.environ['TELEGRAM_CHAT_ID']
TARGET_URL = "https://www.reum.kr/user/pbas/list"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.get(url, params=params)

def check_site():
    # 사이트 데이터 가져오기
    try:
        response = requests.get(TARGET_URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 첫 번째 매물 링크 찾기
        first_item = soup.select_one('a[href*="detail/?pbasCd="]')
        
        if not first_item:
            return

        # 글 번호(ID) 추출
        current_id = first_item['href'].split('=')[-1]
        detail_url = f"https://www.reum.kr/user/pbas/detail/?pbasCd={current_id}"

        # 이전 글 번호와 비교
        if os.path.exists('last_id.txt'):
            with open('last_id.txt', 'r') as f:
                last_id = f.read().strip()
        else:
            last_id = ""

        # 새로운 글이면 알림!
        if current_id != last_id:
            msg = f"📢 *보험잔존물 새 매물 등록!*\n\n🔗 [상세보기 클릭]({detail_url})"
            send_telegram(msg)
            # 현재 번호 저장
            with open('last_id.txt', 'w') as f:
                f.write(current_id)
    except Exception as e:
        print(f"오류 발생: {e}")

if __name__ == "__main__":
    check_site()
