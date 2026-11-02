from fastapi import FastAPI
from pydantic import BaseModel
import joblib


# Load trained AI model
model_data = joblib.load("model.joblib")

model = model_data["model"]
target_names = model_data["target_names"]

app = FastAPI(
    title="AI Model Prediction API",
    description="Iris Flower Prediction Application"
)


# Input data structure
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "AI Model API is running"
    }


# Health check
@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# Prediction endpoint
@app.post("/predict")
def predict(data: IrisInput):

    input_data = [[
        data.sepal_length,
        data.sepal_width,
        data.petal_length,
        data.petal_width
    ]]

    prediction = model.predict(input_data)[0]

    return {
        "prediction": target_names[int(prediction)]
    }