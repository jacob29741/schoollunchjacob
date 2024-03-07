import requests
from instagrapi import Client
import schedule
import time
from datetime import datetime

def get_meal_info():
    url = "https://open.neis.go.kr/hub/mealServiceDietInfo" # 나이스 교육정보 개방 포털 -> 테이터셋 -> 급식식단정보 
    key = "앙" # 나이스 교육정보 개방 포털 -> 활용가이드 -> 인증키 신청

    current_date = datetime.now().strftime('%Y%m%d') # -> 당일 날짜 20240307로 만들고 MLSV_YMD로 ㄷㄱㅈ

    params = {
        'KEY': key,
        'Type': 'json',
        'pIndex': '1',
        'ATPT_OFCDC_SC_CODE': 'S10', # 나이스 교육정보 개방 포털 -> 테이터셋 -> 급식식단정보 -> sheet -> 학교검색 ->  시도교육청코드 붙여넣기
        'SD_SCHUL_CODE': '9010462', # 나이스 교육정보 개방 포털 -> 테이터셋 -> 급식식단정보 -> sheet -> 학교검색 ->  행정표준코드 붙여넣기
        'MLSV_YMD': current_date 
    }

    response = requests.get(url, params=params)
    meal_info = response.json()

    if 'mealServiceDietInfo' in meal_info and 'row' in meal_info['mealServiceDietInfo'][1]:
        for menu in meal_info['mealServiceDietInfo'][1]['row']:
            if 'DDISH_NM' in menu:
                menu['DDISH_NM'] = menu['DDISH_NM'].replace('<br/>', '\n')

    return meal_info

def send_instagram_dm(text, insta_ids):
    try:
        cl = Client()
        cl.login('기모', '링') # 로그인 아이디 / 로그인 비밀번호

        for id in insta_ids:
            try:
                user_id = cl.user_id_from_username(id)
                cl.direct_send(text, user_ids=[user_id])
                print(str(id) + " 계정에게 인스타 DM 발송이 완료되었습니다.")
            except:
                print(str(id) + " 계정에게 인스타 DM 발송이 전송하지 못했습니다.")

        print("최종 DM 발송이 완료되었습니다.")
    except Exception as e:
        print(f"에러가 발생했습니다: {str(e)}")

def combined_job():
    try:
        meal_info = get_meal_info()

        meal_text = "급식 정보:\n"
        for menu in meal_info['mealServiceDietInfo'][1]['row']:
            meal_text += f"- {menu['DDISH_NM']}\n"

        insta_ids = ['ㅅㅅ'] # 보내고 싶은 사람 인스타 아이디
        send_instagram_dm(meal_text, insta_ids)
        
        print("급식 정보 전송이 완료되었습니다.")
    except Exception as e:
        print(f"에러가 발생했습니다: {str(e)}")

# 특정 시간에 급식 보냄.  시간:분:초 없애도 됨 
schedule.every().day.at("21").do(combined_job) 

while True:
    schedule.run_pending()
    time.sleep(1)
