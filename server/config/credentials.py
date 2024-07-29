import os

class ServiceConstant:
    model = "gpt-4o-mini-2024-07-18"
    temperature=0.3
    s3_bucket_name = os.getenv("S3_BUCKET_NAME")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    s3_bucket_url = os.getenv("S3_BUCKET_URL")
    assemblyai_api_key = os.getenv("ASSEMBLYAI_API_KEY")
    langchain_api_key=os.getenv("LANGCHAIN_API_KEY")
    project_name="S2PEDUTECH"