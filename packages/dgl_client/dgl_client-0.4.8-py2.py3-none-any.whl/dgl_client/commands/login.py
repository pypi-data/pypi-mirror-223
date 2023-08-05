import typer
from rich import print
from typing import Optional
from loguru import logger
from .utils import get_inf_client, do_login

app = typer.Typer()

def do_login_web():
    logger.info("Loggin on web")

def do_login_backend():
    logger.info("Loggin on backend")

def do_login_inference():
    logger.info("Loggin on inference server")

@app.callback(invoke_without_command=True)
def login(
  resource: str = typer.Option(default="web")
  ):
    match resource:
        case "web":
            do_login_web()
        case "backend":
            do_login_backend()      
        case "inference":
            do_login_inference()            
        case _:
            logger.error("Invalid login type requested!")
