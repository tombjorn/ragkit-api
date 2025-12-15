import importlib

def load_pipeline_schema(pipeline_name: str):
    try:
        module = importlib.import_module(f"pipelines.{pipeline_name}.schema")
        return module.SCHEMA
    except ModuleNotFoundError:
        return None
