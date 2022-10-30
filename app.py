import re
from databricks import sql
import pandas as pd
from typing import Optional
from urllib import response
from fastapi import FastAPI, Query
import towhee
import uvicorn
import toml
# import faiss
import requests
from types import SimpleNamespace
import json
from fastapi.middleware.cors import CORSMiddleware

props = toml.load("settings.toml")
config = SimpleNamespace(**props.get("e2few"))
dbsql_config = SimpleNamespace(**props.get("adb"))

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

# index = faiss.read_index("halloween_movies_faiss.index")

# def _get_ref_df():
#     """Get reference core plot dataframe from Azure Databricks SQL"""
#     connection = sql.connect(
#                             server_hostname = dbsql_config.dbsql_host,
#                             http_path = dbsql_config.http_path,
#                             access_token = dbsql_config.token)
#     cursor = connection.cursor()
#     query= "select title, genres, plot, core_plot from sgfs.scary_movies;"
#     df  =  pd.read_sql(query, connection)
#     connection.close()
#     return df


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


@app.get("/moviesearch")
def get_movies(utterance: str):
    url = f"{config.host}{config.movie_search_endpoint}"
    payload = json.dumps(dict(instances=[utterance]))
    print(payload)
    headers = {
        "authorization": f"Bearer {config.token}",
        "content-type": "application/json",
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    return json.loads(response.text)