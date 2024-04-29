
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods.media import UploadFile

import info
site_url = "https://titanweapon.com/xmlrpc.php"
username = info.username
password = info.password

# Wordpress 클라이언트 생성
client = Client(site_url,username,password)

# Wordpress 포스트 객체도 생성
post = WordPressPost()

'''
포스팅 내용 생성
'''

title = "여기는 글의 제목입니다"
content = "여기는 글의 내용입니다"

post.title = title

post.post_status = "publish" # 공개로 발행

categories = ["자기계발", "인사이트"]
tags = ["첫글", "태그1"]
post.terms_names = {
    # "key":"value"
    "category" : categories,
    "post_tag" : tags
}

# ------------------------
# 글의 썸네일 등록하는 방법
# ------------------------

image_path = "./thumbnail.png"
image_data = None
#이미지를 바이너리 모드로 읽기
with open(image_path,'rb') as f:
    image_data = f.read()

# 불러온 이미지 데이터 - 워드프레스 사이트 업로드하기
data = {
    "name" : f"{title}.png", # SEO 유리해요. 이미지 검색
    "type" : "image/jpg",
    "caption" : "",
    "description" : f"{title}"
}

data['bits'] = xmlrpc_client.Binary(image_data)

res = client.call(UploadFile(data))
print("이미지 업로드")

thumbnail_id = res['id']
thumbnail_id = int(thumbnail_id)
post.thumbnail = thumbnail_id


# --------------------
# 예약 업로드 기능 추가
# --------------------

from datetime import datetime, timedelta
import pytz

# 서울 시간대 기준으로 만들기
seoul_tz = pytz.timezone("Asia/Seoul")
current_time = datetime.now(seoul_tz)
print(current_time)

# 현재 시간 기준, 3시간 뒤에 포스팅이 발행되도록 하고싶음
reserve_time = current_time + timedelta(hours=0)

# reserve_time : 한국 기준으로 time 설정되있음
# GMT/UTC 시간대로 바꿔줘야 됨
# WordpressPost 클래스 post.date : date 변수가 GMT/UTC 시간대를 넣어주길 기대함
reserve_time = reserve_time.astimezone(pytz.utc)

post.date = reserve_time


# ---------------------
# 글 중간에 이미지 넣는법
# ---------------------

image_path = './apple.jpg'
image_data = None
with open(image_path, 'rb') as f:
    image_data =f.read()

data = {
    "name" : "apple.jpg",
    "type" :"image/jpg",
    "caption" : "Hello image",
    "description" : "apple"
}

data['bits'] = xmlrpc_client.Binary(image_data)

res = client.call(UploadFile(data))
upload_image_link = res['link']

post.content = content + f"<br/> <img src='{upload_image_link}' alt='apple' />" +"<br/> 윗 부분에 이미지가 업로드 잘 되었는지 확인하는 텍스트"


client.call(NewPost(post))
print("포스팅이 업로드 되었습니다.")