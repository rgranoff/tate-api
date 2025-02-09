from fastapi import FastAPI
import pandas as pd
import io
import requests

app = FastAPI()

# ✅ FIX: Removed extra closing bracket
CSV_URLS = {
    "Tate Artist Data": "https://raw.githubusercontent.com/rgranoff/tate-api/main/artist_data.csv",
    "Tate Artwork Data": "https://raw.githubusercontent.com/rgranoff/tate-api/main/artwork_data.csv"
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

        # ✅ FIX: Handle NaN values to avoid JSON errors
        df = df.fillna("")  # Replace NaN with empty strings

        return df.to_dict(orient="records")

    return {"error": "Failed to fetch data"}
