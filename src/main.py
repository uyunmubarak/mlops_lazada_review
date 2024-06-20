import joblib
import mlflow
from fastapi import FastAPI
from pydantic import BaseModel

selected_runs_id = "e4515f7a4d3e4df59e52b2a596cf61db"
logged_model = "runs:/" + selected_runs_id + "/models"
artifacts_path = "vectorizer/vectorizer_2.pkl"
artifacts_dst = "../download/"

app = FastAPI()

class Item(BaseModel):
    reviewContent: list

mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("Lazada Reviews Classification")

loaded_model = mlflow.pyfunc.load_model(logged_model)
mlflow.artifacts.download_artifacts(
    run_id = selected_runs_id,
    artifact_path = artifacts_path,
    dst_path = artifacts_dst
)
vectorizer = joblib.load(artifacts_dst + artifacts_path)

@app.get("/")
def read_root():
    return {"message": "Up!"}

@app.post("/predict")
def predict(item: Item):
    vectorized = vectorizer.transform(item.reviewContent)
    pred = loaded_model.predict(vectorized).tolist()
    return pred