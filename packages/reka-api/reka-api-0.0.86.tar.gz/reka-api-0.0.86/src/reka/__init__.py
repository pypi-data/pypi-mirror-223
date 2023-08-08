"""Reka API."""
import importlib.metadata
import os

# Grab it from an environment variable by default, but can be overriden
API_KEY = os.getenv("REKA_API_KEY")
# Default production server
_SERVER = os.getenv("REKA_SERVER", "https://api.reka.ai")

__version__ = importlib.metadata.version("reka")
from reka.api.chat import chat, vlm_chat
from reka.api.completion import completion
from reka.api.dataset import add_dataset, delete_dataset, list_datasets
from reka.api.retrieval import (
    PrepareRetrievalStatusResponse,
    prepare_retrieval,
    retrieval_job_status,
)
