import json

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import Response

app = FastAPI()


@app.get("/ping")
def ping():
    return {"status": "healthy"}


@app.post("/invocations")
async def predict(request: Request):
    try:
        data = await request.body()  # 这会返回原始的 bytes 数据
        
        # 这里应该是您的模型预测逻辑
        # 这只是一个示例,返回输入数据的长度
        input_data = json.loads(data)
        result = len(input_data["data"])
        response_data = json.dumps({"prediction": result})

        return Response(content=response_data, media_type="application/octet-stream")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
