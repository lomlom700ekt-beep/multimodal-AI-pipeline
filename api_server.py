"""FastAPI сервер для Multimodal AI Pipeline.

Один эндпоинт: POST /analyze — принимает вопрос пользователя,
выполняет два запроса к LLM (SQL + ответ) и возвращает результат.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from analyst import analyze_user_query

app = FastAPI(title="Multimodal AI Pipeline API", version="1.0.0")


class AnalyzeRequest(BaseModel):
    query: str


class AnalyzeResponse(BaseModel):
    result: str


@app.post("/analyze", response_model=AnalyzeResponse, tags=["analyze"])
async def analyze(req: AnalyzeRequest):
    """Принимает вопрос пользователя и возвращает ответ аналитика.

    Внутри выполняется два запроса к LLM:
    1. Генерация SQL-запроса на основе вопроса пользователя.
    2. Формирование текстового ответа на основе данных из базы.
    """
    try:
        result = analyze_user_query(req.query)
        return AnalyzeResponse(result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)