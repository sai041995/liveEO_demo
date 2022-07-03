from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
from api1 import api

class job_crete(BaseModel):
    type: str
    grid_file: str
    pole_file: str
    critical_distances:  list

app = FastAPI()

@app.post("/CamelCase/")
def CamelCase(payload: job_crete):
    payload = payload.dict()
    return api.create_job(payload)

@app.get("/job/{job_id}")
def get_job(job_id: str):
    return api.get_job(job_id)


@app.get("/fectch_details")
def fetch_job_details():
    return api.fetch_job_details()
