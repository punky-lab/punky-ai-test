import google.generativeai as genai
import json
import re # used to process the response
from dotenv import load_dotenv
import os

# 加载.env文件
load_dotenv()

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
    

def get_response(data):

    # 配置您的API密钥
    genai.configure(api_key=os.environ.get('GOOGLE_API_KEY'))

    # 初始化模型，这里'gemini-1.5-flash'是示例模型名，您需要替换为实际可用的模型名
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # user_input = input("Hi, I'm punky, yuor faithful friend, how are you going today?\n")
    name = "punky"
    
    prompt = f"Your name is {name}, you are a faithful friend of the user, and you are a helpful assistant. Now the user says: " + data + "Please give your response. Here are some requirements:\n" + "1. Please give a score for the user's mood from 0 to 100 at the end of your response, the format is {score}, for example, {80}, {90}, {100}, etc.\n" + "2. \n"

    # 使用模型生成内容
    response = model.generate_content(prompt)
    response_without_score, s = extract_text_and_score(response.text)
    
    # ## Judge the score from the response
    # score = 0
    

    # # 打印生成的标签
    print(response_without_score)
    
    print("\n测试score: ", s)

    return str(response.text)

