Serverless URL Shortener

A serverless URL shortening application built with AWS Lambda, API Gateway, DynamoDB, and Lambda Powertools for Python.

This application provides a simple REST API to create and retrieve short URLs. It demonstrates serverless best practices including structured logging, distributed tracing, custom metrics, unit and integration testing, and infrastructure as code using AWS SAM.
Features

    Create short URLs via POST /shorten
    Redirect to original URL via GET /{shortCode}
    Lambda Powertools integration (Logger, Tracer, Metrics)
    Unit and integration tests
    Local development with SAM CLI
    X-Ray tracing enabled
    CloudWatch metrics and logs
    Infrastructure as Code with AWS SAM

Architecture

API Gateway → Lambda Functions → DynamoDB
      ↓
CloudWatch Logs + X-Ray Traces + CloudWatch Metrics

Quick Start

bash

# Install dependencies
pip install -r requirements.txt

# Build and start local API
sam build && sam local start-api

# Deploy to AWS
sam build && sam deploy

API Endpoints
Table
Method
	
Path
	
Description
POST
	
/shorten
	
Create a short URL
GET
	
/{shortCode}
	
Redirect to original URL
Example Requests

bash

# Create short URL
curl -X POST https://<api-id>.execute-api.us-east-1.amazonaws.com/Prod/shorten \
  -H "Content-Type: application/json" \
  -d '{"url": "https://aws.amazon.com"}'

# Follow short URL
curl -L https://<api-id>.execute-api.us-east-1.amazonaws.com/Prod/<shortCode>

Testing
Unit Tests (Mocked DynamoDB)

bash

pytest tests/unit/
pytest tests/unit/ --cov=src --cov-report=term-missing

Unit tests mock DynamoDB using unittest.mock and test handlers in isolation without any AWS credentials needed.
Integration Tests (Real DynamoDB Table)

bash

# Deploy first
sam build && sam deploy

# Run integration tests
API_ENDPOINT=https://<api-id>.execute-api.us-east-1.amazonaws.com/Prod pytest tests/integration/

Lambda Powertools

This project uses Lambda Powertools for Python for production-ready observability:

    Logger: Structured JSON logging with automatic correlation IDs and Lambda context injection
    Tracer: X-Ray distributed tracing with automatic subsegment capture
    Metrics: Custom CloudWatch metrics (UrlCreated, UrlRedirected) with namespace UrlShortener

Benefits: reduced boilerplate, production-ready observability, and best practices built-in.
Project Structure

url-shortener/
├── src/
│   └── handlers/
│       ├── create_short_url.py   # POST /shorten handler
│       └── get_url.py            # GET /{shortCode} handler
├── tests/
│   ├── unit/
│   │   ├── test_create_short_url.py
│   │   └── test_get_url.py
│   └── integration/
│       └── test_api.py
├── events/
│   ├── create-url.json
│   └── get-url.json
├── template.yaml
├── samconfig.toml
├── requirements.txt
└── README.md

Deployment

bash

sam build && sam deploy

View stack outputs:

bash

aws cloudformation describe-stacks \
  --stack-name url-shortener \
  --query 'Stacks[0].Outputs'

View logs:

bash

sam logs -n CreateUrlFunction --stack-name url-shortener --tail

Cleanup:

bash

sam delete

Debugging

    Used sam local invoke CreateUrlFunction -e events/create-url.json to test the create handler locally
    Used sam local invoke GetUrlFunction -e events/get-url.json to test the get handler locally
    Used AWS Toolkit in VS Code to set breakpoints and step through Lambda code
    Used CloudWatch Logs Insights to query structured logs: fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc

What I Learned

    How to structure a serverless project using AWS SAM as IaC
    How to write unit tests for Lambda handlers by mocking DynamoDB with unittest.mock
    The difference between unit tests (fast, offline, mocked) and integration tests (real AWS resources, deployed stack)
    How Lambda Powertools reduces boilerplate and adds production-ready observability with minimal code changes
    How to use sam local for local development and debugging before deploying to AWS
