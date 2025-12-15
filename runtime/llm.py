from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
llm_client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://a3crnf7woihsvzh3.us-east-1.aws.endpoints.huggingface.cloud/v1/"
)
