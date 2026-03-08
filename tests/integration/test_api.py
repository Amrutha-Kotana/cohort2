import requests
import os
import pytest

BASE_URL = os.environ.get("API_ENDPOINT")

@pytest.mark.skipif(not BASE_URL, reason="API_ENDPOINT not set")
def test_create_and_retrieve_url():
    response = requests.post(f"{BASE_URL}/shorten", json={"url": "https://aws.amazon.com"})
    assert response.status_code == 201
    short_code = response.json()["shortCode"]

    redirect = requests.get(f"{BASE_URL}/{short_code}", allow_redirects=False)
    assert redirect.status_code == 301
    assert redirect.headers["Location"] == "https://aws.amazon.com"
