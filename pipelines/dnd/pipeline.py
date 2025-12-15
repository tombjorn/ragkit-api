# pipelines/dnd/pipeline.py
from ragkit import (
    RAGPipeline,
    AugmentationBlock,
    RetrieverBlock,
    GeneratorBlock,
    # Generator,
    StepBack,
    HyDE)
from runtime import (llm_client) 


def get_dnd_pipeline():
    pipeline = (
        RAGPipeline(
            name="dnd",
            llm_client=llm_client,
            client_model="tgi",
            collection_name="dnd",
        )
        # .add(AugmentationBlock, augmentations=[])
        # .add(AugmentationBlock, augmentations=[HyDE(llm_client=llm_client)])
        .add(RetrieverBlock, top_k=3)
        .add(GeneratorBlock)
    )
    return pipeline
