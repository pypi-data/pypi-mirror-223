from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic_settings import BaseSettings 
from pydantic import computed_field

class Settings(BaseSettings):
    PROJECT_NAME: str = "vAST Api Client"

    BACKEND_ENDPOINT: str = "https://www.diglife.eu"
    BACKEND_API_PATH: str = "/api/v1"

    INFERENCE_ENDPOINT: str = "https://www.diglife.eu"
    INFERENCE_API_PATH: str = "/inference"

    WEB_API_KEY: str = ""
    BACKEND_API_KEY: str = ""
    INFERENCE_API_KEY: str = ""

    @computed_field
    @property
    def backend_uri(self) -> str:
        if self.BACKEND_API_PATH:
          return "%s/%s"%(self.BACKEND_ENDPOINT, self.BACKEND_API_PATH)
        return "%s"%(self.BACKEND_ENDPOINT)

    @computed_field
    @property
    def inference_uri(self) -> str:
        if self.INFERENCE_API_PATH:
          return "%s/%s"%(self.INFERENCE_ENDPOINT, self.INFERENCE_API_PATH)
        return "%s"%(self.INFERENCE_ENDPOINT)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        env_nested_delimiter = "__"


settings = Settings()
