from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from process import get_response, extract_text_and_score

app = FastAPI()

class PromptData(BaseModel):
    prompt: str

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/ai_response")
async def get_ai_reply(data: PromptData):
    try:
        # 调用 ai_interface.py 中定义的 get_ai_response 函数
        ai_reply = get_response(data.prompt)
        return {"reply": ai_reply}
    except Exception as e:
        # 如果调用 AI 接口时发生错误，返回 HTTP 500 内部服务器错误
        raise HTTPException(status_code=500, detail=str(e))
