# runtime/pipeline_introspection.py
from typing import Dict, Any
from ragkit.core.pipeline import RAGPipeline


def describe_pipeline(pipeline: RAGPipeline) -> Dict[str, Any]:
    blocks = []

    for block in pipeline.components:
        block_info = {
            "type": block.__class__.__name__,
            "params": {},
        }

        # Extract constructor parameters (best-effort)
        for key, value in vars(block).items():
            if key == "context":
                continue
            if key.startswith("_"):
                continue
            if callable(value):
                continue

            block_info["params"][key] = repr(value)

        # Special cases (augmentations, routing, etc.)
        if hasattr(block, "augmentations"):
            block_info["augmentations"] = [
                aug.__class__.__name__
                for aug in getattr(block, "augmentations", [])
            ]

        if hasattr(block, "routes"):
            block_info["routes"] = list(block.routes.keys())

        blocks.append(block_info)

    return {
        "name": pipeline.name,
        "blocks": blocks,
    }
