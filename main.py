from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from google.cloud import storage

app = FastAPI(title="For Your Service - Pipeline API")

class Scores(BaseModel):
    technical: float
    leadership: float
    temporal: float = Field(default=0.0)
    spatial: float = Field(default=0.0)
    clearance: float = Field(default=0.0)
    preference: float = Field(default=0.0)

class CandidatePayload(BaseModel):
    candidate_id: str
    status: str
    scores: Scores

@app.post("/")
async def ingest_candidate(payload: CandidatePayload):
    try:
        client = storage.Client()
        bucket = client.bucket("fys-landing-dev")
        blob = bucket.blob(f"candidates/{payload.candidate_id}.json")
        blob.upload_from_string(payload.model_dump_json(), content_type="application/json")

        return {
            "status": "success",
            "message": f"Candidate {payload.candidate_id} ingested and stored successfully.",
            "data": payload.model_dump()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "for-your-service-pipeline"}
