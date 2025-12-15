# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipelines.dnd.pipeline import get_dnd_pipeline
from pipelines.dnd.schema import DND_SCHEMA

# from pipelines.business_pipeline import get_pipeline as get_business

app = FastAPI(title="RAGKit API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js dev
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Initialize pipelines ONCE at startup
PIPELINES = {
    "dnd": get_dnd_pipeline(),
    # "business": get_business(),
}

# --- Request Schema ---
class QueryRequest(BaseModel):
    query: str

# --- Routes ---
@app.get("/pipelines")
def list_pipelines():
    return {"pipelines": list(PIPELINES.keys())}

@app.post("/query/{pipeline_name}")
def query_pipeline(pipeline_name: str, body: dict):
    if pipeline_name not in PIPELINES:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    query = body.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Query is required")

    pipeline = PIPELINES[pipeline_name]
    result = pipeline.run(query)

    return {
        "pipeline": pipeline_name,
        "query": query,
        "answer": result.get("answer"),
        "raw": result,
    }


@app.get("/")
def health():
    return {
        "message": "RAGKit API is running",
        "available_endpoints": ["/pipelines", "/query/{pipeline_name}"],
    }


@app.get("/pipelines/{pipeline_name}/schema")
def get_pipeline_schema(pipeline_name: str):
    if pipeline_name == "dnd":
        return DND_SCHEMA
    raise HTTPException(status_code=404, detail="Pipeline not found")
