
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

from wordpress_xmlrpc.compat import xmlrpc_client
from wordpress_xmlrpc.methods.media import UploadFile

import info
import requests

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
post.content = content
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

pixabay_api = info.pixabay_api
query = "사업"

pixabay_url = f"https://pixabay.com/api/?key={pixabay_api}&q={query}&image_type=photo"
response = requests.get(pixabay_url,verify=False)
data = response.json()

if 'hits' in data and len(data['hits']) > 0 : # 이미지 데이터가 존재하면
    import random
    random_image = random.choice(data['hits'])
    image_url = random_image['webformatURL']
    
    image_data = requests.get(image_url,verify=False).content
    
    # 워드프레스 썸네일 등록용 data 만들기
    data = {
        "name" : "사업.jpg",
        "type" : "image/jpg"
    }
    
    data['bits'] = xmlrpc_client.Binary(image_data)
    res = client.call(UploadFile(data))

    thumbnail_id = res['id']
    thumbnail_id = int(thumbnail_id)
    post.thumbnail = thumbnail_id
else:
    # 해당 키워드로 이미지 검색 결과가 없는 경우
    print("# 해당 키워드로 이미지 검색 결과가 없는 경우")


# image_path = "./thumbnail.png"
# image_data = None
# #이미지를 바이너리 모드로 읽기
# with open(image_path,'rb') as f:
#     image_data = f.read()

# # 불러온 이미지 데이터 - 워드프레스 사이트 업로드하기
# data = {
#     "name" : f"{title}.png", # SEO 유리해요. 이미지 검색
#     "type" : "image/jpg",
#     "caption" : "",
#     "description" : f"{title}"
# }

# data['bits'] = xmlrpc_client.Binary(image_data)

# res = client.call(UploadFile(data))
# print("이미지 업로드")

# thumbnail_id = res['id']
# thumbnail_id = int(thumbnail_id)
# post.thumbnail = thumbnail_id

client.call(NewPost(post))
print("포스팅이 업로드 되었습니다.")