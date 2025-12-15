# pipelines/dnd_pipeline.py
from ragkit import (
    RAGPipeline,
    AugmentationBlock,
    RetrieverBlock,
    GeneratorBlock,
    # Generator,
    StepBack,
    HyDE)
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

llm_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://a3crnf7woihsvzh3.us-east-1.aws.endpoints.huggingface.cloud/v1/"
)

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
