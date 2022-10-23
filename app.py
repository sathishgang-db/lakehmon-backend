import re
from databricks import sql
import pandas as pd
from typing import Optional
from urllib import response
from fastapi import FastAPI
import uvicorn
from tabulate import tabulate
import toml
import requests
from types import SimpleNamespace
import json
from fastapi.middleware.cors import CORSMiddleware

config = toml.load("settings.toml")
config = SimpleNamespace(**config.get("e2few"))

app = FastAPI()
app.version = "0.0.1"
app.description = "E2FEW backend for lakehmon"

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://localhost:.*",
    # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.get("/")
def root():
    return {"welcome message": "proceed to /docs to see the list of endpoints! 💁"}



@app.get("/simsearch")
def simsearch(utterance: str):
    url = f"{config.host}{config.sim_search_endpoint}"
    # payload = dict(data=utterance)
    payload = json.dumps(dict(instances=[utterance]))
    print(payload)
    headers = {
        "authorization": f"Bearer {config.token}",
        "content-type": "application/json",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)

