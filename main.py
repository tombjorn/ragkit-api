# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# from pipelines.dnd.pipeline import get_dnd_pipeline
# from pipelines.dnd.schema import SCHEMA

from runtime.schemas import list_blocks, list_augmentations
from runtime.pipeline_introspection import describe_pipeline
from runtime.schema_loader import load_pipeline_schema
from builder.build_pipeline import build_pipeline
from runtime.schema_loader import load_pipeline_schema
app = FastAPI(title="RAGKit API")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# # --- Initialize pipelines ONCE ---
PIPELINES={}

for name in ["dnd", "dnd_complex"]:
    schema = load_pipeline_schema(name)
    PIPELINES[name] = build_pipeline(schema)

# --- Request Models ---
class QueryRequest(BaseModel):
    query: str

# --- Health ---
@app.get("/")
def health():
    return {
        "message": "RAGKit API is running",
        "available_endpoints": [
            "/pipelines",
            "/pipelines/{pipeline_name}",
            "/pipelines/{pipeline_name}/schema",
            "/query/{pipeline_name}",
            "/blocks",
            "/augmentations",
        ],
    }

# --- Pipeline metadata ---
@app.get("/pipelines")
def list_pipelines():
    return {"pipelines": list(PIPELINES.keys())}

@app.get("/pipelines/{pipeline_name}")
def get_pipeline_description(pipeline_name: str):
    pipeline = PIPELINES.get(pipeline_name)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    return describe_pipeline(pipeline)

@app.get("/pipelines/{pipeline_name}/schema")
def get_pipeline_schema(pipeline_name: str):
    schema = load_pipeline_schema(pipeline_name)
    if not schema:
        raise HTTPException(status_code=404, detail="Pipeline schema not found")
    return schema

# --- Registry endpoints ---
@app.get("/blocks")
def get_blocks():
    return list_blocks()

@app.get("/augmentations")
def get_augmentations():
    return {"augmentations": list_augmentations()}

# --- Query execution ---
@app.post("/query/{pipeline_name}")
def query_pipeline(pipeline_name: str, body: QueryRequest):
    pipeline = PIPELINES.get(pipeline_name)
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    result = pipeline.run(body.query)

    return {
        "pipeline": pipeline_name,
        "query": body.query,
        "answer": result.get("answer"),
        "raw": result,
    }
