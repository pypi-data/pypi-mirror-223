from typing import List, Any
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from konko.utils.logs import get_request_json
from konko.utils.utils import get_konko_url
from konko.utils.constants import TIMEOUT
from fastapi import APIRouter, HTTPException, Depends
import os, json

models_router = APIRouter()

class Model(BaseModel):
    id: str = Field(default=None, description="Unique model ID")
    name: str = Field(default=None, description="Name of the model")
    provider: str = Field(default=None, description="Provider of the model")

class ModelMetadata(BaseModel):
    metadata: Any # TODO: Define the actual shape of the metadata object to make it more pertinent to users

api_key_header = APIKeyHeader(name="x-api-key", description="API key to authorize requests")

def get_api_key() -> str:
    if "KONKO_TOKEN" in os.environ:
        return os.environ["KONKO_TOKEN"]
    elif api_key_header:
        return api_key_header
    else:
        raise HTTPException(
            status_code=403, detail="Could not validate credentials. API key should be in the 'x-api-key' header or the 'API_KEY' environment variable."
        )

@models_router.get("/running",
         response_model=List[Model], 
         tags=["Models"],
         summary="RunningModels",
         description="This endpoint retrieves a list of models for all the models running on the Konko instance.",
         )
def running_api(api_key: str = Depends(api_key_header)):

    baseUrl = get_konko_url()
    path = "models/running/"
    url = f"{baseUrl}{path}"
    headers = {"x-api-key": api_key}
    results = get_request_json(url, headers=headers)

    # TODO: Also grab model metadata from the Konko instance.
    # such as decoding parameters, quantization, acceleration, etc.
    # TODO: Once we have generate and embedding, do we keep one model endpoint 
    # or do we have separate model endpoints for each? /generate/model
    # /embedding/models /models /generate /embeddings

    # Convert each result dictionary into a Model object
    model_objects = [Model(**result) for result in results]
    return model_objects

@models_router.get("/running/{model_id}",
                   response_model=ModelMetadata,
                   tags=["Models"],
                   summary="ModelMetadata",
                   description="This endpoint retrieves metadata for a specific model running on the Konko instance.",
                    )
def running_model_metadata_api(model_id: str, api_key: str = Depends(api_key_header)):

    baseUrl = get_konko_url()
    path = f"models/running/{model_id}"
    url = f"{baseUrl}{path}"
    headers = {"x-api-key": api_key}
    model_metadata = get_request_json(url, headers=headers)

    if not model_metadata:
        raise HTTPException(status_code=404, detail="Model not found")

    return model_metadata

def running():
    api_key = get_api_key()
    return running_api(api_key)

def running_model_metadata(model_id):
    model_id = model_id.replace('/', '--')
    api_key = get_api_key()
    return running_model_metadata_api(model_id, api_key)
