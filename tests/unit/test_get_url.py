import json
import pytest
from unittest.mock import patch, MagicMock
import os

os.environ["TABLE_NAME"] = "test-table"
os.environ["POWERTOOLS_SERVICE_NAME"] = "url-shortener"
os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ["POWERTOOLS_METRICS_NAMESPACE"] = "UrlShortener"

from src.handlers.get_url import lambda_handler

class MockContext:
    function_name = "test-function"
    memory_limit_in_mb = 128
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test-function"
    aws_request_id = "test-request-id"

@patch("src.handlers.get_url.table")
def test_get_url_success(mock_table):
    mock_table.get_item = MagicMock(return_value={
        "Item": {"shortCode": "abc12345", "originalUrl": "https://aws.amazon.com"}
    })
    event = {"pathParameters": {"shortCode": "abc12345"}}
    result = lambda_handler(event, MockContext())
    assert result["statusCode"] == 301
    assert result["headers"]["Location"] == "https://aws.amazon.com"

@patch("src.handlers.get_url.table")
def test_get_url_not_found(mock_table):
    mock_table.get_item = MagicMock(return_value={})
    event = {"pathParameters": {"shortCode": "notexist"}}
    result = lambda_handler(event, MockContext())
    assert result["statusCode"] == 404
