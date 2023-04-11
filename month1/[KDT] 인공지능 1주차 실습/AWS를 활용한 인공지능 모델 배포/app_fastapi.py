from typing import List, Dict, Union
from fastapi import FastAPI
from pydantic import BaseModel
from model import MLModelHandler, DLModelHandler
import uvicorn

app = FastAPI()

# assign model handler as global variable [2 LINES]
ml_handler = MLModelHandler()
dl_handler = DLModelHandler()

# 이 위에까지는 flask와 동일하지만 FastAPI에서는 Falsk코드에서 Asynchronous code와 
# Data validation을 위한 부분이 추가 되었음
# define request/response data type for validation
class RequestModel(BaseModel):
    text: Union[str, List[str]]
    model_type: str

class ResponseModel(BaseModel):
    # prediction: {"label":"negative", "score":0.9752}
    # 이렇게 실제 데이터 타입이 어떤 형태로 들어오는지 주석을 달아놓으면 개발을 하고 나중에 다시볼때도 
    # 이렇게 api가 정의가 됫었지 바로바로 확인이 가능하므로 주석 다는 습관을 들이자
    prediction: Dict


@app.get("/")
async def root():
    return {"message": "Hello World"}

# 데코레이터
@app.post("/predict", response_model=ResponseModel)
# 이 request 인자의body정보가 담겨서 들어오는대 바로 호출해서 dict형식으로 들어오기 때문에 
# 바로 request.text코드로 텍스트를 불러올 수있음
async def predict(request: RequestModel):
    text = request.text
    text = [text] if isinstance(text, str) else text
    model_type = request.model_type

    # model inference [2 LINES]
    # await를 명시를 해줘야 ASGI형태의 프로토콜을 따르게 된다.
    # 이렇게 await를 적었더니 에러가 발생해서 await지우고 진행하자
    # if model_type == 'ml':
    #     predictions = await ml_handler.handle(text)
    # else:
    #     predictions = await dl_handler.handle(text)
    
    if model_type == 'ml':
        predictions = ml_handler.handle(text)
    else:
        predictions = dl_handler.handle(text)

    # response
    result = {str(i): {'text': t, 'label': l, 'confidence': c}
                         for i, (t, l, c) in enumerate(zip(text, predictions[0], predictions[1]))}

    return ResponseModel(prediction=result)


if __name__ == '__main__':
    # 플라스크 API와는 다르게 이번에는 8000번 포트로 진행을 해볼것이다.
    # ASGI에선 uvicorn으로 실행을 해주면 된다.
    uvicorn.run(app, host="0.0.0.0", port=8000)
