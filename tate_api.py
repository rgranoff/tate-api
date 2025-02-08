from fastapi import FastAPI
import pandas as pd
import io
import requests

app = FastAPI()

CSV_URLS = {
    "Tate Artist Data": "https://drive.google.com/uc?id=1GOIWXoB7-PPFYCt0FIImFGSm8luIneC",
    "Tate Artwork Data": "https://drive.google.com/uc?id=1agKNrCCPfjnzDLHThrFdnSi1CDIx0RAD",
}

@app.get("/")
def root():
    return {"message": "Welcome to the Tate API! Use /fetch_data/{dataset} to get data."}

@app.get("/fetch_data/{dataset}")
def fetch_data(dataset: str):
    if dataset not in CSV_URLS:
        return {"error": "Dataset not found"}

    url = CSV_URLS[dataset]
    response = requests.get(url)

    if response.status_code == 200:
        df = pd.read_csv(io.StringIO(response.text))

        # **Fix NaN values to prevent JSON error**
        df = df.fillna("")  # Replace NaN with empty strings
        return df.to_dict(orient="records")

    return {"error": "Failed to fetch data"}
