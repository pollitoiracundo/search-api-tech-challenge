from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import numpy as np
from gpt import create_npi_query, get_embeddings_item
from npi import make_npi_api_call
import logging
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

# Define the allowed origins
origins = [
    "http://localhost:3000",  # Frontend local URL
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def healty_call(request: Request):
    return {"message": "success"}

@app.api_route("/search/doctors", methods=["GET", "POST"])
async def search_doctors(request: Request):
    data = await request.body()
    data_str = data.decode('utf-8') 
    #use gpt4o for transform the noisy to a single query
    url = create_npi_query(data_str)
    logger.info(url)
    result = make_npi_api_call(url)
    logger.info(result)
    #result = json.load(result)
    #apply embeddings to each result to add a score
    original_emb = get_embeddings_item(data_str)
    norm_original_emb = np.linalg.norm(original_emb)
    for res in result['results']:
        item_emb = get_embeddings_item(json.dumps(res))
        score = np.dot(original_emb, item_emb) / (norm_original_emb * np.linalg.norm(item_emb)) #https://github.com/openai/openai-cookbook/blob/ed65883e4386d91183dacfbba40dcfcc0f4d00d8/examples/utils/embeddings_utils.py#L64
        res["score"] = score
    return {"message": "success","res": result, "original_input":data_str,"real_query":url}

@app.api_route("/search/clinics", methods=["GET", "POST"])
async def search_clinics(request: Request):
    data = await request.body()
    data_str = data.decode('utf-8') 
    #use gpt4o for transform the noisy to a single query
    url = create_npi_query(data_str)
    logger.info(url)
    result = make_npi_api_call(url)
    logger.info(result)
    #result = json.load(result)
    #apply embeddings to each result to add a score
    original_emb = get_embeddings_item(data_str)
    norm_original_emb = np.linalg.norm(original_emb)
    for res in result['results']:
        item_emb = get_embeddings_item(json.dumps(res))
        score = np.dot(original_emb, item_emb) / (norm_original_emb * np.linalg.norm(item_emb)) #https://github.com/openai/openai-cookbook/blob/ed65883e4386d91183dacfbba40dcfcc0f4d00d8/examples/utils/embeddings_utils.py#L64
        res["score"] = score
    return {"message": "success","res": result, "original_input":data_str,"real_query":url}

#K3lS7TYaPI7N6PdYHDSnr5pUWH119tKr5d6NlIc7