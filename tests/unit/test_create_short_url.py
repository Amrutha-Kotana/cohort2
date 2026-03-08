import json
import pytest
from unittest.mock import patch, MagicMock
import os

os.environ["TABLE_NAME"] = "test-table"
os.environ["POWERTOOLS_SERVICE_NAME"] = "url-shortener"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["POWERTOOLS_METRICS_NAMESPACE"] = "UrlShortener"

from src.handlers.create_short_url import lambda_handler

class MockContext:
    function_name = "test-function"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    aws_request_id = "test-request-id"

@patch("src.handlers.create_short_url.table")
def test_create_short_url_success(mock_table):
    mock_table.put_item = MagicMock()
    event = {"body": json.dumps({"url": "https://aws.amazon.com"})}
    result = lambda_handler(event, MockContext())
    assert result["statusCode"] == 201
    body = json.loads(result["body"])
    assert "shortCode" in body

@patch("src.handlers.create_short_url.table")
def test_create_short_url_missing_url(mock_table):
    event = {"body": json.dumps({})}
    result = lambda_handler(event, MockContext())
    assert result["statusCode"] == 400
