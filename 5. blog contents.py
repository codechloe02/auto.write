import os
import openai
openai.api_key = "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"

def ask_gpt(system, prompt, model="gpt-3.5-turbo"):
  completion = openai.ChatCompletion.create(
    model=model,
    messages=[
      {"role": "system", "content": system},
      {"role": "assistant", "content":"네 알겠습니다."},
      {"role": "user", "content": prompt}
    ],
    stream=True
  )
  result = ""
  

  for chunk in completion:
      delta_data = chunk.choices[0].delta
      if 'role' in delta_data:
          continue
      elif 'content' in delta_data:
          r_text = delta_data['content']
          result += r_text
          print(r_text, end="",flush=True)
  return result

# result = ask_gpt(system="너는 구글 SEO 작가야.",prompt="사과에 대한 블로그 글을 만들어줘.")

# 1. 블로그 글의 제목을 입력하기
title = "사업가에게 휴식이 필요한 이유"

# 2. Chat GPT / GPT-4 : 제목에 적합한 부제목(h2)을 3~4개 생성
title_num = 3 # 부제목 개수
Subtitle_Make_System_Prompt = f''' 
너의 역할은 매우 능숙하게 말하는 SEO 컨텐츠 전문 작가입니다.
내가 너에게 전달해줄 제목을 기반으로 Google 상단에 노출될 블로그 게시물을 작성해줘.
주제와 관련된 부제목을 구체적이고 실용적인 내용을 담아서 부제목을 생성해줘.
누구나 아는 뻔한 내용이 아니라 독특하고 다양한 내용으로 글을 생성해줘.
부제목을 {title_num}개 생성해줘. 생성된 부제목을 python list 결과값으로 돌려주세요.
'''

subtitles = ask_gpt(system=Subtitle_Make_System_Prompt,prompt=title,model="gpt-4")

# 결과값을 파이썬 리스트 자료형으로 만들기 위한 필터링 작업
subtitles = subtitles.strip("][").replace('\n',"").split(",")
def filter_char(m_str):
  # 문자열에서 필터링할 문자를 제거합니다.
  filters = ["[",":",".","]", "," , "_" , "-", "\"", "\'",]
  for char in filters:
    m_str = m_str.replace(char, "")
  return m_str

subtitles = [filter_char(sub_title) for sub_title in subtitles]
print(type(subtitles))
print(subtitles)


# 3. Chat GTP / GPT-3.5 : 생성된 각 부제목을 기반으로 블로그 글을 만들어달라고 요청
Make_Article_System_Prompt = f''' 
너의 역할은 매우 능숙하게 말하는 SEO 컨텐츠 전문 작가입니다.
내가 너에게 전달해줄 부제목에 적합한 문단 내용을 작성해줘.
한글로 1개 혹은 2개의 해시태그를 만들고 기사 맨 끝에 추가해줘.
가능한 한 많고 다양한 컨텐츠로 글을 작성해줘.
중요한 내용은 <strong></strong>태그 사이에 넣어서 강조해줘.
제목, 결론, 요약 내용을 작성하지마.
'''

contents = ""

for subtitle in subtitles:
    subtitle = subtitle.strip()
    print("[서브 글 생성 시작]")
    content = ask_gpt(system=Make_Article_System_Prompt, prompt=subtitle)

    content = f"</br></br> <h2>{subtitle}</h2> </br> {content} </hr>"
    
    contents += content

with open("result.txt","w",encoding="utf8") as f:
  f.write(contents)