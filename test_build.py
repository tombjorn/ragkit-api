# test_build.py
from pipelines.dnd.schema import DND_SCHEMA
from builder.build_pipeline import build_pipeline

pipe = build_pipeline(DND_SCHEMA)
out = pipe.run("What is a beholder?")
print(out["answer"])
