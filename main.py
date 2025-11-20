# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pipelines.dnd_pipeline import get_pipeline
# from pipelines.business_pipeline import get_pipeline as get_business

app = FastAPI(title="RAGKit API")

# Initialize pipelines ONCE at startup
PIPELINES = {
    "dnd": get_pipeline(),
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
def query_pipeline(pipeline_name: str, req: QueryRequest):
    if pipeline_name not in PIPELINES:
        raise HTTPException(status_code=404, detail=f"Pipeline '{pipeline_name}' not found")

    pipeline = PIPELINES[pipeline_name]

    try:
        result = pipeline.run(req.query)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "pipeline": pipeline_name,
        "query": req.query,
        "answer": result.get("answer"),
        "raw": result  # keep raw for debugging
    }

@app.get("/")
def root():
    return {"message": "RAGKit API is running", "available_endpoints": ["/pipelines", "/query/{pipeline_name}"]}
