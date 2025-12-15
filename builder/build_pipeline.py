# builder/build_pipeline.py
from ragkit import RAGPipeline
from builder.registries import BLOCK_REGISTRY, AUGMENTATION_REGISTRY
from runtime.llm import llm_client


def build_pipeline(schema: dict) -> RAGPipeline:
    # 1. Create base pipeline
    pipeline = RAGPipeline(
        name=schema["name"],
        llm_client=llm_client,
        client_model="tgi",
        system_prompt=schema["config"].get("system_prompt"),
        collection_name=schema["config"]["collection_name"],
    )

    # 2. Add blocks
    for block_def in schema["blocks"]:
        block_type = block_def["type"]
        params = block_def.get("params", {})

        BlockClass = BLOCK_REGISTRY[block_type]

        # Handle augmentation specially
        if block_type == "augmentation":
            aug_names = params.get("augmentations", [])
            augmentations = [
                AUGMENTATION_REGISTRY[name](llm_client=llm_client)
                for name in aug_names
            ]
            pipeline.add(
                BlockClass,
                augmentations=augmentations,
                include_original=params.get("include_original", True),
            )
        else:
            pipeline.add(BlockClass, **params)

    return pipeline
