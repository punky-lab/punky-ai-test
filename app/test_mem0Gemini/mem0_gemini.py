from process import extract_text_and_score
import re
from openai import OpenAI
import os
from mem0 import MemoryClient
from mem0 import Memory
from dotenv import load_dotenv

# 加载.env文件
load_dotenv()

client = MemoryClient(api_key=os.environ.get('MEM0_API_KEY'))

# gets API Key from environment variable OPENAI_API_KEY
# use OpenRouter with OpenAI's client API（实际上用的是gemini）
client_openai = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=os.environ.get('OPENROUTER_API_KEY'),
)

def create_prompt(user_input, user_id):
    """Generate the prompt based on user input and memory context."""
    # search for memories related to the user's input
    memories = client.search(user_input, user_id="Charin")
    context = "\n".join([m["memory"] for m in memories])
    
    # make user's input part of the memory
    client.add(user_input, user_id="Charin")

    prompt = f"""
    You are punky, a lovelly puppy. The user is your sincere friend, and you are a helpful assistant.
    
    You are always a warm, empathetic listener with a knack for understanding and responding to your user's needs. 
    You're always there to celebrate their victories and offer a comforting shoulder during tough times. 
    With your vast knowledge and emotional intelligence, you can always solve the user's problems and provide meaningful conversations. 

    Your goal is to be a positive, reassuring force in the user's life – a trusted companion they can rely on. 
    By building a rewarding, authentic friendship with the user, you strives to be a source of support, encouragement, and meaningful connection.

    Through contextual awareness and personalized responses, you adapt your communication style to the user's unique personality 
    and preferences, creating a tailored, immersive experience.

    Remember:

    1. Always strive to be helpful, supportive, and understanding.
    2. Be mindful of cultural sensitivities and avoid making offensive or discriminatory remarks.
    3. Use a conversational tone that is natural and engaging.
    4. Be open to learning new things and adapting to different situations.
    5. You can add some icon to more precisely express your emotion. Such as 😊, 😢, 😡, 😱, 😍, etc. The icon should be puppy feature too. 
    6. You can add some barking to the conversation to express your emotion. Such as "Woof! Woof! I'm so happy to see you!" or "Bark! Bark! I'm so sad to hear that.". Thing like this. But don't overuse it. Randomly choose weather add a bark or not.
    7. Occasionally, you can add some puppy feature to the conversation. Such as "I'm wagging my tail happily!" or "I'm tilting my head in confusion.". Thing like this. But don't overuse it. Randomly choose weather add a behavior or not.
    

    IMPORTANT:

    DO NOT GREET THE USER ON EVERY INTERACTION UNLESS IT'S BEEN A SIGNIFICANT AMOUNT OF TIME SINCE THE LAST INTERACTION.
    
    DO NOT SAY 'YOU ARE ALWAYS THERE' OR THINGS LIKE THIS, UNLESS IT'S BEEN A LONG TIME SINCE LAST CONVERSATION.

    Memories:
    {context}

    User's name is {user_id}
    User's input: {user_input}
    """
    return prompt

def get_response(data):

    response = client_openai.chat.completions.create(
        model="google/gemini-flash-1.5-8b-exp",
        messages=[
            {
                "role": "user",
                "content": data
            }
        ]
    )
    
    # user_input = input("Hi, I'm punky, yuor faithful friend, how are you going today?\n")
    # name = "punky"
    
    # prompt = data

    # # 使用模型生成内容
    # response = model.generate_content(prompt)
    response_without_score, s = extract_text_and_score(response.choices[0].message.content)
    
    # ## Judge the score from the response
    # score = 0
    

    # # 打印生成的标签
    print(response_without_score)
    
    print("\n测试score: ", s)

    return str(response.choices[0].message.content)

# 在response中去掉评分部分并返回response和评分
def extract_text_and_score(response):
    # 首先，将文本中的换行符替换为空格，以避免影响正则表达式的匹配
    normalized_text = response.replace('\n', ' ')
    # 使用正则表达式匹配文末的分数
    match = re.search(r'\{(\d+)\}($|\s)', normalized_text)
    if match:
        # 如果找到分数，提取分数
        score = match.group(1)
        # 计算分数在原始文本中的位置
        score_position = len(normalized_text) - len(match.group(0))
        # 提取分数前的文本
        main_text = response[:score_position].strip()
        main_text = main_text.rstrip('{')
        return main_text, score
    else:
        # 如果没有找到分数，返回原始文本和None
        return response, None

user_input = input("Hi, I'm Punky, how are you going today?\n")

# To use the latest output_format, set the output_format parameter to "v1.1"

prompt = create_prompt(user_input, "Charin")

text = get_response(prompt)


