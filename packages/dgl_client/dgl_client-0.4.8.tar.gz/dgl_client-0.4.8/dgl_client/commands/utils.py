import os
from loguru import logger
from ..config import settings
from ..api_cli import APIClient, InferenceClient, BackendClient


def get_inf_client(endpoint: str = settings.INFERENCE_ENDPOINT, url: str=settings.INFERENCE_API_PATH, debug=False) -> InferenceClient:
  #if url: endpoint = os.path.join(endpoint, url)
  endpoint = settings.inference_uri
  logger.info("Connecting to API Endpoint %s"%endpoint)
  client = InferenceClient(backend_url=endpoint, debug=debug)    
  return client

def get_back_client(endpoint: str = settings.BACKEND_ENDPOINT, url: str = settings.BACKEND_API_PATH, debug=False) -> BackendClient:
  #if url: endpoint = os.path.join(endpoint, url)
  endpoint = settings.backend_uri
  logger.info("Connecting to API Endpoint %s"%endpoint)
  client = BackendClient(backend_url=endpoint, debug=debug)    
  return client

def do_login(access_key, client):
  if access_key:
    return client.login(access_key)
  return False  