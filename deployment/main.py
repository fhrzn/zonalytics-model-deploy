from fastapi import FastAPI
import preprocess
import prediction

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World! - This message was sent from FastAPI"}

@app.get("/sentiment/cleaning")
async def cleaning_debug(text: str):
    return {'output': preprocess.clean(text)}

@app.get("/sentiment")
async def make_prediction(text: str):
    return prediction.predict(text)