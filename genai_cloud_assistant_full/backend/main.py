import os
import re
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from model.qa import get_genai_response  # Your GenAI integration function

load_dotenv()

app = FastAPI(
    title="GenAI AWS Cloud Assistant",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in prod!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    prompt: str

def extract_region(prompt: str) -> str:
    # Default region fallback
    match = re.search(r"\b(us-[a-z]+-[0-9])\b", prompt)
    return match.group(1) if match else "us-east-1"

def detect_services(prompt: str) -> set:
    # Detect which AWS services the prompt references
    prompt_lower = prompt.lower()
    services = set()
    if "ec2" in prompt_lower:
        services.add("ec2")
    if "s3" in prompt_lower:
        services.add("s3")
    if "lambda" in prompt_lower:
        services.add("lambda")
    # Add more services as needed
    return services

def query_ec2(region: str):
    try:
        ec2_client = boto3.client('ec2', region_name=region)
        reservations = ec2_client.describe_instances()['Reservations']
        return [
            {
                'InstanceId': i['InstanceId'],
                'InstanceType': i['InstanceType'],
                'State': i['State']['Name'],
                'AvailabilityZone': i['Placement']['AvailabilityZone']
            }
            for r in reservations for i in r['Instances']
        ]
    except (BotoCoreError, ClientError) as e:
        return {"error": f"EC2 query failed: {str(e)}"}

def query_s3():
    try:
        s3_client = boto3.client('s3')
        buckets = s3_client.list_buckets()['Buckets']
        return [
            {
                'Name': b['Name'],
                'CreationDate': b['CreationDate'].isoformat()
            }
            for b in buckets
        ]
    except (BotoCoreError, ClientError) as e:
        return {"error": f"S3 query failed: {str(e)}"}

@app.post("/query")
def handle_user_query(user_query: UserQuery):
    prompt = user_query.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    region = extract_region(prompt)
    services = detect_services(prompt)

    # Default response containers
    response_data = {"region": region}

    # Query only requested services
    if "ec2" in services:
        response_data["ec2_instances"] = query_ec2(region)
    if "s3" in services:
        response_data["s3_buckets"] = query_s3()
    # Add other services query calls here if needed

    # GenAI analysis of the prompt (or enrich as needed)
    try:
        genai_result = get_genai_response(prompt)
        response_data["genai_analysis"] = genai_result
    except Exception as e:
        response_data["genai_analysis"] = {"error": f"GenAI analysis failed: {str(e)}"}

    return response_data
