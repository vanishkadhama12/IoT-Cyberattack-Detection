import time
import fastapi
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

app = FastAPI(
    title="IoT Cyberattack Detection API",
    description="ML-based network traffic classification",
    version="1.0"
)
# Prometheus monitoring metrics
REQUEST_COUNT = Counter(
    "iot_api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "iot_api_request_latency_seconds",
    "API request processing time"
)
@app.middleware("http")
async def monitor_requests(request, call_next):
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    REQUEST_LATENCY.observe(duration)

    return response
@app.get("/metrics")
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Load trained model
model = joblib.load("models/iot_attack_model.pkl")


class NetworkTraffic(BaseModel):
    packet_count: int
    bytes_sent: int
    bytes_received: int
    connection_duration: float
    failed_connections: int


@app.get("/")
def home():
    return {"message": "IoT Cyberattack Detection API is running!"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict")
def predict(data: NetworkTraffic):
    input_data = pd.DataFrame([data.model_dump()])

    prediction = int(model.predict(input_data)[0])

    if prediction == 1:
        result = "Suspicious Traffic"
    else:
        result = "Normal Traffic"

    return {
        "prediction": prediction,
        "result": result
    }
