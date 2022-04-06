import os
import requests
import json
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
from twython import Twython
from datetime import datetime
from pytz import timezone
from github_utils import get_github_repo, upload_github_issue


if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "git-action-weather-alert"

    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")

    try:
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_argument("lang=ko_KR")
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("--no-sandbox")

        # chrome driver
        driver = webdriver.Chrome('chromedriver', chrome_options=options)
        driver.implicitly_wait(3)

        # 케이웨더 접속
        driver.get('https://www.kweather.co.kr/weather.html')
        driver.maximize_window()    

        kweather_map = driver.find_element(By.CLASS_NAME, "w_map")

        location = kweather_map.location
        size = kweather_map.size

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']
        sleep(3)
    
        png = driver.get_screenshot_as_png()
        img = Image.open(BytesIO(png))
        # 오늘의 날씨 영역만 잘라냅니다.
        area = (left, top, right, bottom)    
        kweather = img.crop(area)
        kweather.save('./kweather.png')
        photo = open("./kweather.png", 'rb')
        
        #############################################
        # configure twitter API 
        ######################################
        APP_KEY = '0iq5BNj24RSVdeIqdkGtyBxKa' #
        APP_SECRET = '1kyFv4RFDJTsI4wYsDhJkeMO3WBI7UmT41fp949qM8UoscnIvj' #
        OAUTH_TOKEN = '1511732564519632896-42f15OsOJfH1veuRb9WvvHDkxoef3k' #
        OAUTH_TOKEN_SECRET = '2I1vCR2MyBrDGSqgm7blIQYMqe9OaslKPxfvOuJ2TUzJ4' #
        
        ###################
        # upload twitter
        ##################
        twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
        # 트위터에 잘라낸 오늘의 날씨 영역 이미지를 업로드 합니다.
        response = twitter.upload_media(media=photo)
        tweet_message = 'kweather'
        result = twitter.update_status(status=tweet_message, media_ids=[response['media_id']])
        photo_url = result['extended_entities']['media'][0]['media_url_https']
        
        photo = "![weather](" + photo_url + ")"

        issue_title = f"{today_date} 날씨 알림"
        upload_contents = photo
        repo = get_github_repo(access_token, repository_name)
        upload_github_issue(repo, issue_title, upload_contents)
        print("Upload Github Issue Success!")

    except Exception as e:
        print(e)
        driver.quit()
    
    finally:
        print('finally.')
        driver.quit()
