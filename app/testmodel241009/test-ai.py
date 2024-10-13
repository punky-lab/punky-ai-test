from openai import OpenAI
from openai import OpenAI
import os
from mem0 import MemoryClient
from mem0 import Memory
from dotenv import load_dotenv
from create_prompt import create_prompt

# 加载.env文件
load_dotenv()

mem0client = MemoryClient(api_key=os.environ.get('MEM0_API_KEY'))

# gets API Key from environment variable OPENAI_API_KEY
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get("OPENROUTER_API_KEY"),
)

# input prompt
input_prompt = input("Hi~ I'm Punky, how is it going?\n")
while True:
  if input_prompt:
    
    completion = client.chat.completions.create(
      extra_headers={
        "HTTP-Referer": "http://localhost:3000", # Optional, for including your app on openrouter.ai rankings.
        "X-Title": "TestAIModel", # Optional. Shows in rankings on openrouter.ai.
      },
      # model="liquid/lfm-40b",
      # model="google/gemini-flash-1.5-8b", # nice for chat
      # model = "liquid/lfm-40b:free", 
      # model = "anthracite-org/magnum-v2-72b",
      # model = "meta-llama/llama-3.2-3b-instruct:free", # nice for chat
      model = "google/gemini-pro-1.5-exp",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": create_prompt(input_prompt, "Hurricane")
            },
          ]
        }
      ]
    )
    print(completion.choices[0].message.content)
    input_prompt = None
    
    input_prompt = input()


