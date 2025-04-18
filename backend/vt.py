import os
import requests

def scan_url(url):
    api_key = os.getenv("VT_API_KEY")
    if not api_key:
        raise ValueError("VT_API_KEY not set in environment")

    headers = {
        "x-apikey": api_key
    }

    response = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers=headers,
        data={"url": url}
    )
    if response.status_code != 200:
        raise Exception(f"Failed to submit URL: {response.text}")

    analysis_id = response.json()["data"]["id"]

    analysis_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    result = requests.get(analysis_url, headers=headers)
    return result.json()
