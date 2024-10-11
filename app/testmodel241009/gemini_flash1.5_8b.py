from openai import OpenAI
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get('OPENROUTER_API_KEY'),
)

# 读取原始prompt
with open('prompt_origin.txt', 'r', encoding='UTF-8') as f:
  prompt_org = f.read()

# input prompt
  input_prompt = input("Hi~ I'm Punky, how is it going?\n")

while True:
  

  completion = client.chat.completions.create(
    extra_headers={
      "HTTP-Referer": os.environ.get('SITE_URL'), # Optional, for including your app on openrouter.ai rankings.
      "X-Title": os.environ.get('SITE_NAME'), # Optional. Shows in rankings on openrouter.ai.
    },
    model="google/gemini-flash-1.5-8b",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": prompt_org + input_prompt
          },
        ]
      }
    ]
  )
  print(completion.choices[0].message.content)
  
  input_prompt = input()


