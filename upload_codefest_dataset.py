import requests
import os

api_key = os.getenv("OPENAI_API_KEY")
dataset_id = "CODEFEST_DATASET_23"
file_paths = ["ASE-proposalweb-dashboard.json",
              "FPL-dashboard.json",
              "logresults-2023-01-26 10_13_03.csv",
              "logresults-2023-01-26 10_13_40.json",
              "pod_data_logresults-2023-01-26-10_41_56.csv"]

# Authenticate the request with an API key

headers = {"Authorization": f"Bearer {api_key}"}

for file_path in file_paths:
    with open(file_path, "rb") as f:
        file_data = f.read()

    url = f"https://api.openapi.com/v1/datasets/{dataset_id}/versions"
    response = requests.post(url, headers=headers, data=file_data)

    # check the status
    if (response.status_code == 201):
        print(f"{file_oath} uploaded successfully")
    else:
        print(f"An error occurred while uploading {file_path}: + {response.text}")