from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

app = FastAPI()

class PredictionInput(BaseModel):
    data: list

@app.get("/ping")
def ping():
    return {"status": "healthy"}

@app.post("/invocations")
def predict(input_data: PredictionInput):
    try:
        # 这里应该是您的模型预测逻辑
        # 这只是一个示例,返回输入数据的长度
        result = len(input_data.data)
        return {"prediction": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
