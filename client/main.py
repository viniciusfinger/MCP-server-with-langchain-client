from fastapi import FastAPI
import uvicorn
import logging
from controller import ask_controller
from config.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(ask_controller.router)

if __name__ == "__main__":
    try:
        uvicorn.run(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Error starting the server: {e}")
        raise e