import os
import openai
openai.api_key = "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"

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "너는 구글 상위노출 글을 작성하는 SEO 전문 컨텐츠 작가야."},
    {"role": "assistant", "content":"네 알겠습니다."},
    {"role": "user", "content": "사과에 관한 블로그 글을 작성해줘."}
  ],
  stream=True
)
result = ""
print(completion)
# print(completion.choices[0].message['content'])
for chunk in completion:
    delta_data = chunk.choices[0].delta
    if 'role' in delta_data:
        continue
    elif 'content' in delta_data:
        r_text = delta_data['content']
        result += r_text
        print(r_text, end="",flush=True)
    
print(result)