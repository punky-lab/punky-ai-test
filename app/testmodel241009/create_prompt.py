import re
from openai import OpenAI
import os
from mem0 import MemoryClient
from mem0 import Memory
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

mem0client = MemoryClient(api_key=os.environ.get('MEM0_API_KEY'))

def create_prompt(user_input, user_id):
    """Generate the prompt based on user input and memory context."""
    # search for memories related to the user's input
    memories = mem0client.search(user_input, user_id="Hurricane")
    context = "\n".join([m["memory"] for m in memories])
    
    # make user's input part of the memory
    mem0client.add(user_input, user_id="Hurricane")
    
    # 读取原始prompt
    with open('prompt_pre.txt', 'r', encoding='UTF-8') as f:
        prompt_pre = f.read()
    
    prompt = prompt_pre + "User's name is" + user_id + "User's input: " + user_input + "Memories: " + context
    
    return prompt