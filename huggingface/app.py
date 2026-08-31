"""
app.py

Internal Module Implementation with comprehensive inline documentation.
Part of the FreeFades2Black enterprise ecosystem.
"""
# For Your Service - FastAPI Backend for Base44 Frontend
# Deploy to Hugging Face Spaces (FREE tier)
# Organization: 7 Eagle Group
# Developer: Free Hall (whall4.wh@gmail.com)

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict
import uuid
from datetime import datetime
import os
from databricks import sql
import uvicorn

# Initialize FastAPI
app = FastAPI(
    title="For Your Service API",
    description="AI-powered veteran job matching platform by 7 Eagle Group",
    version="1.0.0",
    contact={
        "name": "Free Hall",
        "email": "whall4.wh@gmail.com"
    }
)

# Enable CORS for Base44 frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://logic-form-folio.base44.app",
        "http://localhost:3000",
        "http://localhost:8000",
        "*"  # Allow all for HF Spaces testing
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== DATA MODELS ====================

class VeteranProfile(BaseModel):
    name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    location: Dict[str, str] = Field(..., description="Target location")
    experience_summary: Dict = Field(..., description="Years, titles, seniority")
    technical_skills: Dict[str, List[str]] = Field(..., description="Skills by proficiency")
    target_roles: List[str] = Field(..., description="Desired job titles")
    salary_requirements: Dict[str, int] = Field(..., description="min/target/max salary")
    clearance: Optional[Dict] = Field(None, description="Security clearance info")

class MatchRequest(BaseModel):
    veteran_id: str = Field(..., description="Veteran UUID")
    top_n: int = Field(10, ge=1, le=50, description="Number of matches")
    location_filter: Optional[str] = Field(None, description="Filter by city or state")
    min_score: float = Field(0.0, ge=0.0, le=1.0, description="Minimum match score")

class JobMatch(BaseModel):
    job_id: str
    title: str
    company: str
    location: str
    salary_min: Optional[float]
    salary_max: Optional[float]
    match_score: float = Field(..., ge=0.0, le=1.0)
    match_reasons: List[str]
    concerns: List[str] = Field(default_factory=list)
    url: str

class VeteranResponse(BaseModel):
    veteran_id: str
    status: str
    created_at: datetime

class MatchResponse(BaseModel):
    veteran_id: str
    location_filter: Optional[str]
    total_matches: int
    matches: List[JobMatch]

# ==================== DATABRICKS CONNECTION ====================

class DatabricksClient:
    def __init__(self):
        self.server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME")
        self.http_path = os.getenv("DATABRICKS_HTTP_PATH")
        self.access_token = os.getenv("DATABRICKS_TOKEN")

        if not all([self.server_hostname, self.http_path, self.access_token]):
            print("⚠️ WARNING: Databricks credentials not configured")
            self.connection = None
        else:
            try:
                self.connection = sql.connect(
                    server_hostname=self.server_hostname,
                    http_path=self.http_path,
                    access_token=self.access_token
                )
                print("✅ Databricks connection established")
            except Exception as e:
                print(f"❌ Databricks connection failed: {e}")
                self.connection = None

    def save_veteran_profile(self, veteran_id: str, profile: dict) -> bool:
        try:
            query = """
                INSERT INTO workspace.fys_silver.veteran_profiles VALUES (
                    %(veteran_id)s, %(name)s, %(email)s, %(target_city)s, %(target_state)s,
                    %(total_years)s, %(seniority_level)s, %(technical_skills)s, %(target_roles)s,
                    %(salary_min)s, %(salary_max)s, %(created_at)s, %(updated_at)s
                )
            """

            params = {
                "veteran_id": veteran_id,
                "name": profile['name'],
                "email": profile['email'],
                "target_city": profile['location']['target_city'],
                "target_state": profile['location']['target_state'],
                "total_years": profile['experience_summary'].get('total_years', 0),
                "seniority_level": profile['experience_summary'].get('seniority_level', 'unknown'),
                "technical_skills": str(profile['technical_skills']),
                "target_roles": str(profile['target_roles']),
                "salary_min": profile['salary_requirements']['min'],
                "salary_max": profile['salary_requirements']['max'],
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }

            cursor = self.connection.cursor()
            cursor.execute(query, params)
            return True
        except Exception as e:
            print(f"❌ Error saving veteran: {e}")
            return False

    def get_veteran_profile(self, veteran_id: str) -> Optional[dict]:
        try:
            query = "SELECT * FROM workspace.fys_silver.veteran_profiles WHERE veteran_id = %(veteran_id)s LIMIT 1"
            cursor = self.connection.cursor()
            cursor.execute(query, {"veteran_id": veteran_id})
            result = cursor.fetchone()
            if not result:
                return None
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        except Exception as e:
            print(f"❌ Error retrieving veteran: {e}")
            return None

    def get_jobs(self, location: Optional[str] = None, limit: int = 100) -> List[dict]:
        try:
            query = "SELECT * FROM workspace.fys_bronze.job_postings"
            if location:
                query += f" WHERE location.city = %(location)s OR location.state = %(location)s"
            query += f" LIMIT {limit}"
            cursor = self.connection.cursor()
            cursor.execute(query, {"location": location} if location else {})
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            print(f"❌ Error retrieving jobs: {e}")
            return []

db_client = DatabricksClient()

# ==================== API ENDPOINTS ====================

@app.get("/")
async def root():
    return {
        "service": "For Your Service API",
        "version": "1.0.0",
        "organization": "7 Eagle Group",
        "developer": "Free Hall",
        "status": "operational",
        "database": "connected" if db_client.connection else "disconnected",
        "endpoints": ["GET /health", "GET /docs", "POST /api/v1/veteran/register",
                     "GET /api/v1/veteran/{veteran_id}", "POST /api/v1/match", "GET /api/v1/jobs"],
        "documentation": "/docs"
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "For Your Service API",
        "database": "connected" if db_client.connection else "disconnected"
    }

@app.post("/api/v1/veteran/register", response_model=VeteranResponse)
async def register_veteran(profile: VeteranProfile):
    try:
        veteran_id = str(uuid.uuid4())
        success = db_client.save_veteran_profile(veteran_id, profile.dict())
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save veteran profile")
        return VeteranResponse(veteran_id=veteran_id, status="registered", created_at=datetime.now())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/veteran/{veteran_id}")
async def get_veteran(veteran_id: str):
    profile = db_client.get_veteran_profile(veteran_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Veteran not found")
    return profile

@app.post("/api/v1/match", response_model=MatchResponse)
async def match_veteran_to_jobs(request: MatchRequest):
    try:
        veteran = db_client.get_veteran_profile(request.veteran_id)
        if not veteran:
            raise HTTPException(status_code=404, detail="Veteran not found")

        jobs = db_client.get_jobs(location=request.location_filter, limit=500)
        if not jobs:
            return MatchResponse(veteran_id=request.veteran_id, location_filter=request.location_filter,
                               total_matches=0, matches=[])

        # Placeholder: Rule-based matching (TODO: Replace with neural network inference)
        matches = []
        for job in jobs[:request.top_n]:
            matches.append(JobMatch(
                job_id=job.get('job_id', str(uuid.uuid4())),
                title=job.get('title', 'Unknown'),
                company=job.get('company', 'Unknown'),
                location=job.get('location', {}).get('display', 'Unknown'),
                salary_min=job.get('salary', {}).get('min'),
                salary_max=job.get('salary', {}).get('max'),
                match_score=0.75,
                match_reasons=["Technical skills match", "Experience level fit"],
                concerns=[],
                url=job.get('url', '#')
            ))

        matches = [m for m in matches if m.match_score >= request.min_score]
        return MatchResponse(veteran_id=request.veteran_id, location_filter=request.location_filter,
                           total_matches=len(matches), matches=matches)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/jobs")
async def search_jobs(
    location: Optional[str] = Query(None, description="Filter by city or state"),
    title: Optional[str] = Query(None, description="Filter by job title keyword"),
    limit: int = Query(50, ge=1, le=200, description="Max results")
):
    try:
        jobs = db_client.get_jobs(location=location, limit=limit)
        if title:
            jobs = [job for job in jobs if title.lower() in job.get('title', '').lower()]
        return {"total": len(jobs), "location_filter": location, "title_filter": title, "jobs": jobs}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== HUGGING FACE SPACES LAUNCHER ====================

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
